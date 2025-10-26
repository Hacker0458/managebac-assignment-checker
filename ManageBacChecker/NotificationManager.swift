//
//  NotificationManager.swift
//  ManageBacChecker
//
//  Created by Assistant on 2025/9/29.
//

import Foundation
import UserNotifications
import SwiftUI

// MARK: - 通知管理器
@MainActor
class NotificationManager: ObservableObject {
    static let shared = NotificationManager()
    
    @Published var isAuthorized = false
    @Published var authorizationStatus: UNAuthorizationStatus = .notDetermined
    
    private let notificationCenter = UNUserNotificationCenter.current()
    
    private init() {
        checkAuthorizationStatus()
    }
    
    // MARK: - 权限管理
    func requestAuthorization() async -> Bool {
        do {
            let granted = try await notificationCenter.requestAuthorization(options: [.alert, .sound, .badge])
            await MainActor.run {
                self.isAuthorized = granted
                self.authorizationStatus = granted ? .authorized : .denied
            }
            
            if granted {
                print("✅ 通知权限已授权")
            } else {
                print("❌ 通知权限被拒绝")
            }
            
            return granted
        } catch {
            print("❌ 请求通知权限失败: \(error)")
            return false
        }
    }
    
    func checkAuthorizationStatus() {
        notificationCenter.getNotificationSettings { settings in
            DispatchQueue.main.async {
                self.authorizationStatus = settings.authorizationStatus
                self.isAuthorized = settings.authorizationStatus == .authorized
            }
        }
    }
    
    // MARK: - 作业提醒通知
    func scheduleAssignmentReminders(for assignments: [Assignment]) {
        guard isAuthorized else {
            print("⚠️ 通知权限未授权，无法安排提醒")
            return
        }
        
        // 清除现有的通知
        clearAllNotifications()
        
        let unsubmittedAssignments = assignments.filter { $0.status == .notSubmitted }
        
        for assignment in unsubmittedAssignments {
            scheduleNotificationForAssignment(assignment)
        }
        
        print("📱 已为 \(unsubmittedAssignments.count) 个未提交作业安排提醒")
    }
    
    private func scheduleNotificationForAssignment(_ assignment: Assignment) {
        guard let dueDate = assignment.dueDate else { return }
        
        let now = Date()
        
        // 安排多个提醒时间点
        let reminderIntervals: [TimeInterval] = [
            24 * 3600,  // 1天前
            12 * 3600,  // 12小时前
            6 * 3600,   // 6小时前
            3600        // 1小时前
        ]
        
        for (index, interval) in reminderIntervals.enumerated() {
            let reminderDate = dueDate.addingTimeInterval(-interval)
            
            // 只安排未来的提醒
            if reminderDate > now {
                let identifier = "\(assignment.id.uuidString)-\(index)"
                scheduleNotification(
                    identifier: identifier,
                    title: getNotificationTitle(for: assignment, interval: interval),
                    body: getNotificationBody(for: assignment, interval: interval),
                    date: reminderDate,
                    assignment: assignment
                )
            }
        }
        
        // 安排截止时间通知
        if dueDate > now {
            let identifier = "\(assignment.id.uuidString)-due"
            scheduleNotification(
                identifier: identifier,
                title: "作业即将截止！",
                body: "\(assignment.title) 即将在 \(assignment.subject) 课程中截止",
                date: dueDate,
                assignment: assignment
            )
        }
    }
    
    private func scheduleNotification(
        identifier: String,
        title: String,
        body: String,
        date: Date,
        assignment: Assignment
    ) {
        let content = UNMutableNotificationContent()
        content.title = title
        content.body = body
        content.sound = .default
        content.badge = 1
        
        // 添加自定义数据
        content.userInfo = [
            "assignmentId": assignment.id.uuidString,
            "assignmentTitle": assignment.title,
            "subject": assignment.subject,
            "priority": assignment.priority.rawValue
        ]
        
        // 设置通知类别和操作
        content.categoryIdentifier = "ASSIGNMENT_REMINDER"
        
        let trigger = UNCalendarNotificationTrigger(
            dateMatching: Calendar.current.dateComponents([.year, .month, .day, .hour, .minute], from: date),
            repeats: false
        )
        
        let request = UNNotificationRequest(identifier: identifier, content: content, trigger: trigger)
        
        notificationCenter.add(request) { error in
            if let error = error {
                print("❌ 安排通知失败: \(error)")
            } else {
                print("✅ 成功安排通知: \(title) at \(date)")
            }
        }
    }
    
    private func getNotificationTitle(for assignment: Assignment, interval: TimeInterval) -> String {
        let hours = Int(interval / 3600)
        
        switch hours {
        case 24:
            return "作业提醒 - 1天后截止"
        case 12:
            return "作业提醒 - 12小时后截止"
        case 6:
            return "作业提醒 - 6小时后截止"
        case 1:
            return "紧急提醒 - 1小时后截止！"
        default:
            return "作业提醒"
        }
    }
    
    private func getNotificationBody(for assignment: Assignment, interval: TimeInterval) -> String {
        let hours = Int(interval / 3600)
        let timeString = hours >= 24 ? "\(hours/24)天" : "\(hours)小时"
        
        return "\(assignment.title) 将在 \(timeString) 后截止，请及时完成提交。科目：\(assignment.subject)"
    }
    
    // MARK: - 通知管理
    func clearAllNotifications() {
        notificationCenter.removeAllPendingNotificationRequests()
        notificationCenter.removeAllDeliveredNotifications()
        print("🗑️ 已清除所有通知")
    }
    
    func clearNotificationsForAssignment(_ assignmentId: UUID) {
        notificationCenter.getPendingNotificationRequests { requests in
            let identifiersToRemove = requests
                .filter { $0.content.userInfo["assignmentId"] as? String == assignmentId.uuidString }
                .map { $0.identifier }
            
            Task { @MainActor in
                self.notificationCenter.removePendingNotificationRequests(withIdentifiers: identifiersToRemove)
                print("🗑️ 已清除作业 \(assignmentId) 的 \(identifiersToRemove.count) 个通知")
            }
        }
    }
    
    func getPendingNotificationsCount() async -> Int {
        let requests = await notificationCenter.pendingNotificationRequests()
        return requests.count
    }
    
    // MARK: - 每日摘要通知
    func scheduleDailySummary(assignments: [Assignment]) {
        guard isAuthorized else { return }
        
        let unsubmittedCount = assignments.filter { $0.status == .notSubmitted }.count
        let overdueCount = assignments.filter { 
            $0.status == .notSubmitted && 
            ($0.dueDate ?? Date.distantFuture) < Date() 
        }.count
        
        guard unsubmittedCount > 0 else { return }
        
        let content = UNMutableNotificationContent()
        content.title = "每日作业摘要"
        content.body = "您有 \(unsubmittedCount) 个未完成作业"
        if overdueCount > 0 {
            content.body += "，其中 \(overdueCount) 个已过期"
        }
        content.sound = .default
        content.badge = NSNumber(value: unsubmittedCount)
        content.categoryIdentifier = "DAILY_SUMMARY"
        
        // 设置每天早上8点提醒
        var dateComponents = DateComponents()
        dateComponents.hour = 8
        dateComponents.minute = 0
        
        let trigger = UNCalendarNotificationTrigger(dateMatching: dateComponents, repeats: true)
        let request = UNNotificationRequest(identifier: "daily-summary", content: content, trigger: trigger)
        
        notificationCenter.add(request) { error in
            if let error = error {
                print("❌ 安排每日摘要失败: \(error)")
            } else {
                print("✅ 已安排每日摘要通知")
            }
        }
    }
    
    // MARK: - 通知操作处理
    func setupNotificationActions() {
        // 作业提醒通知的操作
        let markCompleteAction = UNNotificationAction(
            identifier: "MARK_COMPLETE",
            title: "标记完成",
            options: [.foreground]
        )
        
        let viewDetailsAction = UNNotificationAction(
            identifier: "VIEW_DETAILS",
            title: "查看详情",
            options: [.foreground]
        )
        
        let snoozeAction = UNNotificationAction(
            identifier: "SNOOZE",
            title: "稍后提醒",
            options: []
        )
        
        let assignmentCategory = UNNotificationCategory(
            identifier: "ASSIGNMENT_REMINDER",
            actions: [markCompleteAction, viewDetailsAction, snoozeAction],
            intentIdentifiers: [],
            options: []
        )
        
        // 每日摘要通知的操作
        let openAppAction = UNNotificationAction(
            identifier: "OPEN_APP",
            title: "打开应用",
            options: [.foreground]
        )
        
        let summaryCategory = UNNotificationCategory(
            identifier: "DAILY_SUMMARY",
            actions: [openAppAction],
            intentIdentifiers: [],
            options: []
        )
        
        notificationCenter.setNotificationCategories([assignmentCategory, summaryCategory])
    }
}

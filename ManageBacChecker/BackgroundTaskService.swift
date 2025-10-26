//
//  BackgroundTaskService.swift
//  ManageBac Assignment Checker
//
//  Created by 方籽杰 on 2025/9/26.
//  后台任务服务 - 处理后台刷新和通知
//

import Foundation
import BackgroundTasks
import UIKit
import UserNotifications

// MARK: - 后台任务服务
class BackgroundTaskService: ObservableObject {
    static let shared = BackgroundTaskService()

    // 后台任务标识符
    private let backgroundRefreshTaskID = "com.managebac.checker.refresh"
    private let backgroundNotificationTaskID = "com.managebac.checker.notifications"

    private init() {
        registerBackgroundTasks()
    }

    // MARK: - 注册后台任务
    private func registerBackgroundTasks() {
        // 注册后台刷新任务
        BGTaskScheduler.shared.register(forTaskWithIdentifier: backgroundRefreshTaskID, using: nil) { task in
            self.handleBackgroundRefresh(task: task as! BGAppRefreshTask)
        }

        // 注册后台通知任务
        BGTaskScheduler.shared.register(forTaskWithIdentifier: backgroundNotificationTaskID, using: nil) { task in
            self.handleBackgroundNotification(task: task as! BGProcessingTask)
        }
    }

    // MARK: - 调度后台任务
    func scheduleBackgroundRefresh() {
        let request = BGAppRefreshTaskRequest(identifier: backgroundRefreshTaskID)
        request.earliestBeginDate = Date(timeIntervalSinceNow: 15 * 60) // 15分钟后

        do {
            try BGTaskScheduler.shared.submit(request)
            print("📱 后台刷新任务已调度")
        } catch {
            print("❌ 调度后台刷新失败: \(error)")
        }
    }

    func scheduleBackgroundNotification() {
        let request = BGProcessingTaskRequest(identifier: backgroundNotificationTaskID)
        request.earliestBeginDate = Date(timeIntervalSinceNow: 60 * 60) // 1小时后
        request.requiresNetworkConnectivity = true
        request.requiresExternalPower = false

        do {
            try BGTaskScheduler.shared.submit(request)
            print("📱 后台通知任务已调度")
        } catch {
            print("❌ 调度后台通知失败: \(error)")
        }
    }

    // MARK: - 处理后台任务
    private func handleBackgroundRefresh(task: BGAppRefreshTask) {
        print("🔄 执行后台刷新任务")

        // 调度下一次后台刷新
        scheduleBackgroundRefresh()

        // 创建任务操作
        let refreshOperation = BackgroundRefreshOperation()

        task.expirationHandler = {
            refreshOperation.cancel()
            print("⏰ 后台刷新任务超时")
        }

        refreshOperation.completionBlock = {
            task.setTaskCompleted(success: !refreshOperation.isCancelled)
            print("✅ 后台刷新任务完成")
        }

        // 执行刷新操作
        OperationQueue().addOperation(refreshOperation)
    }

    private func handleBackgroundNotification(task: BGProcessingTask) {
        print("🔔 执行后台通知任务")

        // 调度下一次后台通知检查
        scheduleBackgroundNotification()

        // 创建通知检查操作
        let notificationOperation = BackgroundNotificationOperation()

        task.expirationHandler = {
            notificationOperation.cancel()
            print("⏰ 后台通知任务超时")
        }

        notificationOperation.completionBlock = {
            task.setTaskCompleted(success: !notificationOperation.isCancelled)
            print("✅ 后台通知任务完成")
        }

        // 执行通知操作
        OperationQueue().addOperation(notificationOperation)
    }
}

// MARK: - 后台刷新操作
class BackgroundRefreshOperation: Operation, @unchecked Sendable {
    override func main() {
        guard !isCancelled else { return }

        // 创建一个信号量来等待异步操作完成
        let semaphore = DispatchSemaphore(value: 0)

        Task {
            await performBackgroundRefresh()
            semaphore.signal()
        }

        // 等待操作完成或取消
        while !isCancelled && semaphore.wait(timeout: .now() + 30) == .timedOut {
            // 继续等待或处理超时
        }
    }

    @MainActor
    private func performBackgroundRefresh() async {
        // 获取共享的AssignmentManager实例
        let assignmentManager = AssignmentManager()

        // 仅在配置正确时执行刷新
        guard !assignmentManager.config.email.isEmpty,
              !assignmentManager.config.password.isEmpty else {
            print("⚠️ 后台刷新跳过：未配置账户信息")
            return
        }

        // 执行作业刷新
        await assignmentManager.fetchAssignments()

        // 检查是否有紧急作业需要立即通知
        let urgentAssignments = assignmentManager.assignments.filter { assignment in
            guard let dueDate = assignment.dueDate else { return false }
            let hoursUntilDue = dueDate.timeIntervalSinceNow / 3600
            return hoursUntilDue <= 24 && hoursUntilDue > 0 && assignment.status == .notSubmitted
        }

        if !urgentAssignments.isEmpty {
            NotificationService.shared.sendUrgentAssignmentNotification(assignments: urgentAssignments)
        }

        print("🔄 后台刷新完成：找到 \(assignmentManager.assignments.count) 个作业")
    }
}

// MARK: - 后台通知操作
class BackgroundNotificationOperation: Operation, @unchecked Sendable {
    override func main() {
        guard !isCancelled else { return }

        let semaphore = DispatchSemaphore(value: 0)

        Task {
            await performNotificationCheck()
            semaphore.signal()
        }

        while !isCancelled && semaphore.wait(timeout: .now() + 15) == .timedOut {
            // 继续等待
        }
    }

    private func performNotificationCheck() async {
        // 检查即将到期的作业并发送通知
        await NotificationService.shared.checkAndSendDueReminders()
        print("🔔 后台通知检查完成")
    }
}

// MARK: - 通知服务
@MainActor
class NotificationService: ObservableObject {
    static let shared = NotificationService()

    private let notificationCenter = UNUserNotificationCenter.current()

    private init() {
        setupNotificationCategories()
    }

    // MARK: - 设置通知类别
    private func setupNotificationCategories() {
        // 创建通知动作
        let markCompleteAction = UNNotificationAction(
            identifier: "MARK_COMPLETE",
            title: "标记完成",
            options: [.foreground]
        )

        let snoozeAction = UNNotificationAction(
            identifier: "SNOOZE",
            title: "稍后提醒",
            options: []
        )

        // 创建通知类别
        let assignmentCategory = UNNotificationCategory(
            identifier: "ASSIGNMENT_REMINDER",
            actions: [markCompleteAction, snoozeAction],
            intentIdentifiers: [],
            options: [.customDismissAction]
        )

        notificationCenter.setNotificationCategories([assignmentCategory])
    }

    // MARK: - 权限请求
    func requestNotificationPermission() async -> Bool {
        do {
            let granted = try await notificationCenter.requestAuthorization(options: [.alert, .badge, .sound, .provisional])
            print("通知权限: \(granted ? "已授权" : "被拒绝")")
            return granted
        } catch {
            print("请求通知权限失败: \(error)")
            return false
        }
    }

    // MARK: - 发送通知
    func sendUrgentAssignmentNotification(assignments: [Assignment]) {
        guard !assignments.isEmpty else { return }

        let content = UNMutableNotificationContent()
        content.categoryIdentifier = "ASSIGNMENT_REMINDER"

        if assignments.count == 1 {
            let assignment = assignments[0]
            content.title = "📚 作业提醒"
            content.body = "「\(assignment.title)」即将到期"
            content.subtitle = assignment.subject
        } else {
            content.title = "📚 多个作业提醒"
            content.body = "您有 \(assignments.count) 个作业即将到期"
            content.subtitle = "点击查看详情"
        }

        content.sound = .default
        content.badge = NSNumber(value: assignments.filter { $0.status == .notSubmitted }.count)

        // 添加自定义数据
        content.userInfo = [
            "assignments": assignments.map { $0.id.uuidString },
            "type": "urgent_reminder"
        ]

        // 立即发送通知
        let trigger = UNTimeIntervalNotificationTrigger(timeInterval: 1, repeats: false)
        let request = UNNotificationRequest(
            identifier: "urgent_\(UUID().uuidString)",
            content: content,
            trigger: trigger
        )

        notificationCenter.add(request) { error in
            if let error = error {
                print("发送紧急通知失败: \(error)")
            } else {
                print("✅ 紧急通知已发送")
            }
        }
    }

    func scheduleAssignmentReminder(for assignment: Assignment, hoursBeforeDue: Int = 24) {
        guard let dueDate = assignment.dueDate else { return }

        let reminderDate = dueDate.addingTimeInterval(-TimeInterval(hoursBeforeDue * 3600))

        // 只为未来的日期安排通知
        guard reminderDate > Date() else { return }

        let content = UNMutableNotificationContent()
        content.categoryIdentifier = "ASSIGNMENT_REMINDER"
        content.title = "📚 作业提醒"
        content.body = "「\(assignment.title)」将在 \(hoursBeforeDue) 小时后到期"
        content.subtitle = assignment.subject
        content.sound = .default

        content.userInfo = [
            "assignmentId": assignment.id.uuidString,
            "type": "scheduled_reminder"
        ]

        let calendar = Calendar.current
        let dateComponents = calendar.dateComponents([.year, .month, .day, .hour, .minute], from: reminderDate)
        let trigger = UNCalendarNotificationTrigger(dateMatching: dateComponents, repeats: false)

        let request = UNNotificationRequest(
            identifier: "reminder_\(assignment.id.uuidString)_\(hoursBeforeDue)h",
            content: content,
            trigger: trigger
        )

        notificationCenter.add(request) { error in
            if let error = error {
                print("安排提醒失败: \(error)")
            } else {
                print("✅ 已安排 \(assignment.title) 的提醒通知")
            }
        }
    }

    func sendDailySummaryNotification(assignments: [Assignment]) {
        let unsubmittedCount = assignments.filter { $0.status == .notSubmitted }.count
        let todayDueCount = assignments.filter { assignment in
            guard let dueDate = assignment.dueDate else { return false }
            return Calendar.current.isDateInToday(dueDate)
        }.count

        guard unsubmittedCount > 0 || todayDueCount > 0 else { return }

        let content = UNMutableNotificationContent()
        content.title = "📊 每日作业摘要"

        var bodyComponents: [String] = []
        if unsubmittedCount > 0 {
            bodyComponents.append("\(unsubmittedCount) 个未提交作业")
        }
        if todayDueCount > 0 {
            bodyComponents.append("\(todayDueCount) 个今日到期")
        }

        content.body = bodyComponents.joined(separator: "，")
        content.sound = .default
        content.badge = NSNumber(value: unsubmittedCount)

        content.userInfo = [
            "type": "daily_summary",
            "unsubmittedCount": unsubmittedCount,
            "todayDueCount": todayDueCount
        ]

        let trigger = UNTimeIntervalNotificationTrigger(timeInterval: 1, repeats: false)
        let request = UNNotificationRequest(
            identifier: "daily_summary_\(Date().timeIntervalSince1970)",
            content: content,
            trigger: trigger
        )

        notificationCenter.add(request) { error in
            if let error = error {
                print("发送每日摘要失败: \(error)")
            } else {
                print("✅ 每日摘要通知已发送")
            }
        }
    }

    // MARK: - 检查和发送到期提醒
    func checkAndSendDueReminders() async {
        // 获取当前作业数据
        let assignmentManager = AssignmentManager()

        // 查找需要提醒的作业
        let now = Date()
        let reminderThresholds: [TimeInterval] = [
            24 * 3600,  // 24小时
            6 * 3600,   // 6小时
            1 * 3600    // 1小时
        ]

        for assignment in assignmentManager.assignments {
            guard assignment.status == .notSubmitted,
                  let dueDate = assignment.dueDate,
                  dueDate > now else { continue }

            let timeUntilDue = dueDate.timeIntervalSince(now)

            for threshold in reminderThresholds {
                if timeUntilDue <= threshold && timeUntilDue > threshold - 3600 {
                    // 在阈值范围内，发送提醒
                    let hoursBeforeDue = Int(threshold / 3600)
                    scheduleAssignmentReminder(for: assignment, hoursBeforeDue: hoursBeforeDue)
                }
            }
        }
    }

    // MARK: - 清理通知
    func clearAllNotifications() {
        notificationCenter.removeAllPendingNotificationRequests()
        notificationCenter.removeAllDeliveredNotifications()
        UNUserNotificationCenter.current().setBadgeCount(0)
        print("🧹 所有通知已清理")
    }

    func clearNotificationsFor(assignment: Assignment) {
        let identifiersToRemove = [
            "reminder_\(assignment.id.uuidString)_24h",
            "reminder_\(assignment.id.uuidString)_6h",
            "reminder_\(assignment.id.uuidString)_1h"
        ]

        notificationCenter.removePendingNotificationRequests(withIdentifiers: identifiersToRemove)
        print("🧹 已清理 \(assignment.title) 的通知")
    }
}

// MARK: - App生命周期扩展
extension ManageBacCheckerApp {
    func setupBackgroundTasks() {
        // 应用进入后台时调度后台任务
        NotificationCenter.default.addObserver(
            forName: UIApplication.didEnterBackgroundNotification,
            object: nil,
            queue: .main
        ) { _ in
            BackgroundTaskService.shared.scheduleBackgroundRefresh()
            BackgroundTaskService.shared.scheduleBackgroundNotification()
        }

        // 应用变为活跃时取消待定的后台任务
        NotificationCenter.default.addObserver(
            forName: UIApplication.didBecomeActiveNotification,
            object: nil,
            queue: .main
        ) { _ in
            // 应用变为活跃时，取消待定的后台任务并执行前台刷新
            BGTaskScheduler.shared.cancel(taskRequestWithIdentifier: "com.managebac.checker.refresh")
        }
    }
}
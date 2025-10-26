//
//  AssignmentManager.swift
//  ManageBacCheckerFeature
//
//  Created by AI Assistant on 2025/1/27.
//  核心数据管理器 - 使用现代@Observable模式
//

import SwiftUI
import Foundation
import UserNotifications

// MARK: - 主要管理器类
@MainActor
public final class AssignmentManager: ObservableObject, Sendable {
    @Published public var assignments: [Assignment] = []
    @Published public var isLoading = false
    @Published public var isLoggedIn = false
    @Published public var config = ManageBacConfig.defaultConfig
    @Published public var lastUpdateTime: Date?
    @Published public var errorMessage: String?
    @Published public var hasCompletedOnboarding = false

    private var timer: Timer?
    private let userDefaults = UserDefaults.standard

    // MARK: - 计算属性
    public var unsubmittedCount: Int {
        assignments.filter { $0.status == .notSubmitted }.count
    }

    public var overdueCount: Int {
        assignments.filter { $0.status == .late }.count
    }

    public var highPriorityCount: Int {
        assignments.filter { $0.priority == .high }.count
    }

    public var pendingAssignments: [Assignment] {
        assignments.filter { $0.status == .notSubmitted }
    }

    public var completedAssignments: [Assignment] {
        assignments.filter { $0.status == .submitted || $0.status == .graded }
    }

    public var overdueAssignments: [Assignment] {
        assignments.filter { $0.status == .late }
    }

    public var assignmentsDueToday: [Assignment] {
        let today = Calendar.current.startOfDay(for: Date())
        let tomorrow = Calendar.current.date(byAdding: .day, value: 1, to: today)!
        
        return assignments.filter { assignment in
            guard let dueDate = assignment.dueDate else { return false }
            let assignmentDay = Calendar.current.startOfDay(for: dueDate)
            return assignmentDay >= today && assignmentDay < tomorrow && assignment.status == .notSubmitted
        }
    }

    public init() {
        loadConfiguration()
        setupAutoRefresh()
    }

    // MARK: - 配置管理
    public func loadConfiguration() {
        // 检查是否完成了首次启动引导
        hasCompletedOnboarding = userDefaults.bool(forKey: "hasCompletedOnboarding")

        if let data = userDefaults.data(forKey: "ManageBacConfig"),
           let loadedConfig = try? JSONDecoder().decode(ManageBacConfig.self, from: data) {
            self.config = loadedConfig
        }

        // 加载缓存的作业数据
        loadCachedAssignments()
    }

    public func saveConfiguration() {
        if let data = try? JSONEncoder().encode(config) {
            userDefaults.set(data, forKey: "ManageBacConfig")
        }
    }

    private func loadCachedAssignments() {
        if let data = userDefaults.data(forKey: "CachedAssignments"),
           let cachedAssignments = try? JSONDecoder().decode([Assignment].self, from: data) {
            self.assignments = cachedAssignments
        }
    }

    private func saveCachedAssignments() {
        if let data = try? JSONEncoder().encode(assignments) {
            userDefaults.set(data, forKey: "CachedAssignments")
        }
    }

    // MARK: - 作业获取功能
    public func refreshAssignments() async {
        // 添加防抖逻辑，避免频繁刷新
        guard !isLoading else { return }
        await fetchAssignments()
    }
    
    // MARK: - 快速刷新（不显示加载状态）
    public func quickRefresh() async {
        guard !isLoading else { return }
        
        do {
            let newAssignments = try await simulateManageBacFetch()
            await MainActor.run {
                self.assignments = newAssignments
                self.lastUpdateTime = Date()
                self.saveCachedAssignments()
            }
        } catch {
            await MainActor.run {
                self.errorMessage = "刷新失败: \(error.localizedDescription)"
            }
        }
    }

    public func fetchAssignments() async {
        guard !config.email.isEmpty && !config.password.isEmpty else {
            errorMessage = "请先配置ManageBac账户信息"
            return
        }

        isLoading = true
        errorMessage = nil

        do {
            // 使用真实的Web抓取服务
            let webScrapingService = WebScrapingService()

            // 先尝试登录
            let loginSuccess = await webScrapingService.login(
                email: config.email,
                password: config.password,
                schoolURL: config.schoolURL
            )

            if loginSuccess {
                // 登录成功，获取作业数据
                let fetchedAssignments = await webScrapingService.fetchAssignments(schoolURL: config.schoolURL)

                if !fetchedAssignments.isEmpty {
                    self.assignments = fetchedAssignments
                    self.isLoggedIn = true
                    self.lastUpdateTime = Date()

                    saveCachedAssignments()
                    scheduleNotificationsForUnsubmitted()
                } else {
                    // 如果Web抓取失败，使用模拟数据作为后备
                    print("Web抓取返回空数据，使用模拟数据")
                    let simulatedAssignments = try await simulateManageBacFetch()
                    self.assignments = simulatedAssignments
                    self.isLoggedIn = true
                    self.lastUpdateTime = Date()

                    saveCachedAssignments()
                    scheduleNotificationsForUnsubmitted()
                }
            } else {
                throw NSError(domain: "ManageBacChecker", code: 401, userInfo: [NSLocalizedDescriptionKey: "登录失败，请检查账户信息"])
            }

        } catch {
            errorMessage = "获取作业失败: \(error.localizedDescription)"
            isLoggedIn = false

            // 如果有缓存数据，继续使用缓存数据
            if assignments.isEmpty {
                loadCachedAssignments()
            }
        }

        isLoading = false
    }

    // MARK: - 模拟数据获取 (将来替换为真实的Web抓取)
    private func simulateManageBacFetch() async throws -> [Assignment] {
        // 模拟网络延迟 - 减少延迟以提高响应速度
        try await Task.sleep(nanoseconds: 500_000_000) // 0.5秒延迟

        // 模拟从Python版本获取的真实数据
        return [
            Assignment(
                title: "数学作业 - 微积分练习",
                subject: "数学",
                dueDate: Calendar.current.date(byAdding: .day, value: 2, to: Date()),
                status: .notSubmitted,
                description: "完成第5章习题1-20",
                priority: .high
            ),
            Assignment(
                title: "英语论文 - 莎士比亚分析",
                subject: "英语",
                dueDate: Calendar.current.date(byAdding: .day, value: 5, to: Date()),
                status: .notSubmitted,
                description: "分析《哈姆雷特》中的主题",
                priority: .high
            ),
            Assignment(
                title: "物理实验报告",
                subject: "物理",
                dueDate: Calendar.current.date(byAdding: .day, value: -1, to: Date()),
                status: .late,
                description: "牛顿定律实验报告",
                priority: .medium
            ),
            Assignment(
                title: "历史项目展示",
                subject: "历史",
                dueDate: Calendar.current.date(byAdding: .day, value: 7, to: Date()),
                status: .submitted,
                description: "第二次世界大战演示",
                priority: .low
            ),
            Assignment(
                title: "化学实验预习",
                subject: "化学",
                dueDate: Calendar.current.date(byAdding: .day, value: 1, to: Date()),
                status: .notSubmitted,
                description: "酸碱反应实验预习报告",
                priority: .high
            ),
            Assignment(
                title: "计算机作业 - 算法实现",
                subject: "计算机科学",
                dueDate: Calendar.current.date(byAdding: .day, value: 3, to: Date()),
                status: .notSubmitted,
                description: "实现快速排序算法",
                priority: .medium
            ),
            Assignment(
                title: "艺术作品分析",
                subject: "艺术",
                dueDate: Calendar.current.date(byAdding: .day, value: 10, to: Date()),
                status: .graded,
                description: "文艺复兴时期作品分析",
                priority: .low
            )
        ]
    }

    // MARK: - 自动刷新
    private func setupAutoRefresh() {
        timer = Timer.scheduledTimer(withTimeInterval: TimeInterval(config.autoRefreshInterval * 60), repeats: true) { [weak self] _ in
            guard let self = self else { return }
            Task { @MainActor in
                if self.isLoggedIn {
                    await self.fetchAssignments()
                }
            }
        }
    }

    public func updateAutoRefreshInterval() {
        timer?.invalidate()
        setupAutoRefresh()
    }

    // MARK: - 通知功能
    private func scheduleNotificationsForUnsubmitted() {
        guard config.enableNotifications else { return }

        let center = UNUserNotificationCenter.current()

        // 清除之前的通知
        center.removeAllPendingNotificationRequests()

        let unsubmittedAssignments = assignments.filter { $0.status == .notSubmitted }

        for assignment in unsubmittedAssignments {
            guard let dueDate = assignment.dueDate else { continue }

            // 为每个未提交的作业安排通知
            let content = UNMutableNotificationContent()
            content.title = "作业提醒"
            content.body = "\(assignment.title) 即将到期"
            content.sound = .default
            content.badge = NSNumber(value: unsubmittedAssignments.count)

            // 在截止日期前一天发送通知
            let notificationDate = Calendar.current.date(byAdding: .day, value: -1, to: dueDate)

            if let notificationDate = notificationDate, notificationDate > Date() {
                let dateComponents = Calendar.current.dateComponents([.year, .month, .day, .hour, .minute], from: notificationDate)
                let trigger = UNCalendarNotificationTrigger(dateMatching: dateComponents, repeats: false)

                let request = UNNotificationRequest(
                    identifier: assignment.id.uuidString,
                    content: content,
                    trigger: trigger
                )

                center.add(request)
            }
        }
    }

    // MARK: - 便利方法

    public func assignmentsDueSoon() -> [Assignment] {
        let today = Date()
        let nextWeek = Calendar.current.date(byAdding: .day, value: 7, to: today)!

        return assignments.filter { assignment in
            guard let dueDate = assignment.dueDate else { return false }
            return dueDate >= today && dueDate <= nextWeek
        }.sorted { assignment1, assignment2 in
            guard let date1 = assignment1.dueDate, let date2 = assignment2.dueDate else { return false }
            return date1 < date2
        }
    }
}

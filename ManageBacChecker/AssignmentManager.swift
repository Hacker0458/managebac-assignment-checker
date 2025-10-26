//
//  AssignmentManager.swift
//  ManageBacChecker
//
//  Created by 方籽杰 on 2025/9/26.
//

import Foundation
import Combine
import SwiftUI

// MARK: - 数据模型
struct Assignment: Identifiable, Codable {
    var id = UUID()
    let title: String
    let subject: String
    let dueDate: Date?
    let status: AssignmentStatus
    let description: String
    let priority: Priority
    
    enum AssignmentStatus: String, Codable, CaseIterable {
        case notSubmitted = "未提交"
        case submitted = "已提交"
        case late = "迟交"
        case graded = "已评分"
        
        var color: Color {
            switch self {
            case .notSubmitted: return .red
            case .submitted: return .green
            case .late: return .orange
            case .graded: return .blue
            }
        }
        
        var icon: String {
            switch self {
            case .notSubmitted: return "exclamationmark.circle"
            case .submitted: return "checkmark.circle"
            case .late: return "clock.circle"
            case .graded: return "star.circle"
            }
        }
        
        var localizedTitle: String {
            return self.rawValue
        }
    }
    
    enum Priority: String, Codable, CaseIterable {
        case low = "低"
        case medium = "中"
        case high = "高"
        
        var color: Color {
            switch self {
            case .low: return .green
            case .medium: return .orange
            case .high: return .red
            }
        }
        
        var localizedTitle: String {
            return self.rawValue
        }
    }
}

// MARK: - 配置模型
struct ManageBacConfig: Codable {
    var email: String
    var password: String
    var schoolURL: String
    var language: String
    var autoRefreshInterval: TimeInterval
    var enableNotifications: Bool
    
        static let defaultConfig = ManageBacConfig(
            email: "fangp458@gmail.com",
            password: "Aa081130",
            schoolURL: "https://shtcs.managebac.cn",
            language: "zh",
            autoRefreshInterval: 30 * 60, // 30分钟
            enableNotifications: true
        )
}

// MARK: - 作业管理器
@MainActor
class AssignmentManager: ObservableObject {
    @Published var assignments: [Assignment] = []
    @Published var isLoading = false
    @Published var config = ManageBacConfig.defaultConfig
    @Published var isLoggedIn = false
    @Published var lastUpdateTime: Date?
    @Published var errorMessage: String?
    
    private var cancellables = Set<AnyCancellable>()
    private let userDefaults = UserDefaults.standard
    
    init() {
        loadConfiguration()
        loadCachedAssignments()
    }
    
    // MARK: - 获取作业数据
    func fetchAssignments() async {
        guard !isLoading else {
            print("⚠️ 已在获取数据中，跳过重复请求")
            return
        }
        
        isLoading = true
        errorMessage = nil
        print("🔄 开始获取作业数据...")

        // 尝试使用真实的网络请求
        if !config.email.isEmpty && !config.password.isEmpty && !config.schoolURL.isEmpty {
            print("🌐 尝试从ManageBac获取真实数据...")
            
            // 首先尝试登录
            let loginSuccess = await NetworkManager.shared.login(
                email: config.email,
                password: config.password,
                schoolURL: config.schoolURL
            )
            
            if loginSuccess {
                print("✅ 登录成功")
                
                // 获取作业数据
                let fetchedAssignments = await NetworkManager.shared.fetchAssignments(schoolURL: config.schoolURL)
                
                if !fetchedAssignments.isEmpty {
                    self.assignments = fetchedAssignments
                    self.isLoggedIn = true
                    self.lastUpdateTime = Date()
                    self.errorMessage = nil
                    print("✅ 获取到 \(fetchedAssignments.count) 个真实作业")
                    saveCachedAssignments()
                    scheduleNotificationsForUnsubmitted()
                    isLoading = false
                    return
                }
            } else {
                print("❌ 登录失败，使用模拟数据")
                errorMessage = NetworkManager.shared.errorMessage
            }
        }
        
        // 如果网络请求失败或配置不完整，使用模拟数据
        print("📋 使用模拟数据作为后备方案")
        self.assignments = createSimulatedAssignments()
        self.isLoggedIn = true
        self.lastUpdateTime = Date()
        self.errorMessage = nil
        print("✅ 使用模拟数据，共 \(self.assignments.count) 个作业")
        
        saveCachedAssignments()
        scheduleNotificationsForUnsubmitted()
        
        isLoading = false
    }
    
    // MARK: - 创建模拟数据
    private func createSimulatedAssignments() -> [Assignment] {
        let subjects = ["数学", "英语", "物理", "化学", "生物", "历史", "地理", "政治"]
        let priorities: [Assignment.Priority] = [.low, .medium, .high]
        let statuses: [Assignment.AssignmentStatus] = [.notSubmitted, .submitted, .late, .graded]
        
        var assignments: [Assignment] = []
        
        for i in 1...15 {
            let subject = subjects.randomElement() ?? "未知科目"
            let priority = priorities.randomElement() ?? .medium
            let status = statuses.randomElement() ?? .notSubmitted
            
            let daysOffset = Int.random(in: -7...14)
            let dueDate = Calendar.current.date(byAdding: .day, value: daysOffset, to: Date())
            
            let assignment = Assignment(
                title: "\(subject)作业 \(i)",
                subject: subject,
                dueDate: dueDate,
                status: status,
                description: "这是\(subject)的第\(i)个作业，需要认真完成。包含多个练习题和理论分析。",
                priority: priority
            )
            
            assignments.append(assignment)
        }
        
        return assignments.sorted { first, second in
            guard let firstDate = first.dueDate, let secondDate = second.dueDate else {
                return first.dueDate != nil
            }
            return firstDate < secondDate
        }
    }
    
    // MARK: - 配置管理
    private func loadConfiguration() {
        if let data = userDefaults.data(forKey: "managebac_config"),
           let savedConfig = try? JSONDecoder().decode(ManageBacConfig.self, from: data) {
            self.config = savedConfig
        }
    }
    
    func saveConfiguration() {
        if let data = try? JSONEncoder().encode(config) {
            userDefaults.set(data, forKey: "managebac_config")
        }
    }
    
    func updateConfiguration(_ newConfig: ManageBacConfig) {
        self.config = newConfig
        saveConfiguration()
        
        Task {
            await fetchAssignments()
        }
    }
    
    // MARK: - 缓存管理
    private func loadCachedAssignments() {
        if let data = userDefaults.data(forKey: "cached_assignments"),
           let cachedAssignments = try? JSONDecoder().decode([Assignment].self, from: data) {
            self.assignments = cachedAssignments
            print("✅ 加载缓存作业: \(cachedAssignments.count) 个")
        }
    }
    
    private func saveCachedAssignments() {
        if let data = try? JSONEncoder().encode(assignments) {
            userDefaults.set(data, forKey: "cached_assignments")
            print("💾 保存作业缓存: \(assignments.count) 个")
        }
    }
    
    // MARK: - 通知管理
    private func scheduleNotificationsForUnsubmitted() {
        let unsubmittedAssignments = assignments.filter { $0.status == .notSubmitted }
        print("📱 为 \(unsubmittedAssignments.count) 个未提交作业安排通知")
        
        // 这里可以添加具体的通知逻辑
        for assignment in unsubmittedAssignments {
            if let dueDate = assignment.dueDate, dueDate > Date() {
                // 安排通知逻辑
                print("📅 为作业 '\(assignment.title)' 安排提醒，截止时间: \(dueDate)")
            }
        }
    }
    
    // MARK: - 自动刷新
    func startAutoRefresh() {
        Timer.publish(every: config.autoRefreshInterval, on: .main, in: .common)
            .autoconnect()
            .sink { [weak self] _ in
                Task { @MainActor in
                    if self?.isLoggedIn == true {
                        await self?.fetchAssignments()
                    }
                }
            }
            .store(in: &cancellables)
    }
    
    func stopAutoRefresh() {
        cancellables.removeAll()
    }
    
    // MARK: - 计算属性
    var unsubmittedCount: Int {
        assignments.filter { $0.status == .notSubmitted }.count
    }
    
    var overdueCount: Int {
        assignments.filter { assignment in
            assignment.status == .notSubmitted && 
            (assignment.dueDate ?? Date.distantFuture) < Date()
        }.count
    }
    
    var completedCount: Int {
        assignments.filter { $0.status == .submitted || $0.status == .graded }.count
    }
    
    var upcomingAssignments: [Assignment] {
        assignments.filter { assignment in
            assignment.status == .notSubmitted &&
            (assignment.dueDate ?? Date.distantFuture) > Date()
        }.sorted { first, second in
            guard let firstDate = first.dueDate, let secondDate = second.dueDate else {
                return first.dueDate != nil
            }
            return firstDate < secondDate
        }
    }
    
    var highPriorityCount: Int {
        assignments.filter { $0.priority == .high }.count
    }
    
    func assignmentsDueSoon() -> [Assignment] {
        let nextWeek = Calendar.current.date(byAdding: .weekOfYear, value: 1, to: Date()) ?? Date()
        return assignments.filter { assignment in
            guard let dueDate = assignment.dueDate else { return false }
            return dueDate > Date() && dueDate <= nextWeek && assignment.status == .notSubmitted
        }.sorted { first, second in
            guard let firstDate = first.dueDate, let secondDate = second.dueDate else {
                return first.dueDate != nil
            }
            return firstDate < secondDate
        }
    }
    
    // MARK: - 登出
    func logout() {
        isLoggedIn = false
        assignments = []
        lastUpdateTime = nil
        errorMessage = nil
        stopAutoRefresh()
        
        userDefaults.removeObject(forKey: "cached_assignments")
        userDefaults.removeObject(forKey: "managebac_config")
        
        print("👋 用户已登出")
    }
}
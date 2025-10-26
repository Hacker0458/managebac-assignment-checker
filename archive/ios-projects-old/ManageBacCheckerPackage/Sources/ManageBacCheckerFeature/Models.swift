//
//  Models.swift
//  ManageBacCheckerFeature
//
//  Created by AI Assistant on 2025/1/27.
//  数据模型定义
//

import SwiftUI
import Foundation

// MARK: - 作业数据模型
public struct Assignment: Identifiable, Codable, Sendable {
    public let id: UUID
    public let title: String
    public let subject: String
    public let dueDate: Date?
    public let status: AssignmentStatus
    public let description: String
    public let priority: Priority

    public init(
        title: String,
        subject: String,
        dueDate: Date? = nil,
        status: AssignmentStatus,
        description: String,
        priority: Priority
    ) {
        self.id = UUID()
        self.title = title
        self.subject = subject
        self.dueDate = dueDate
        self.status = status
        self.description = description
        self.priority = priority
    }

    public enum AssignmentStatus: String, Codable, CaseIterable, Sendable {
        case notSubmitted = "notSubmitted"
        case submitted = "submitted"
        case late = "late"
        case graded = "graded"

        public var localizedTitle: String {
            switch self {
            case .notSubmitted: return "未提交"
            case .submitted: return "已提交"
            case .late: return "逾期"
            case .graded: return "已评分"
            }
        }

        public var color: Color {
            switch self {
            case .notSubmitted: return .red
            case .submitted: return .green
            case .late: return .orange
            case .graded: return .blue
            }
        }

        public var icon: String {
            switch self {
            case .notSubmitted: return "exclamationmark.triangle"
            case .submitted: return "checkmark.circle"
            case .late: return "clock.badge.exclamationmark"
            case .graded: return "star.circle"
            }
        }
    }

    public enum Priority: String, Codable, CaseIterable, Sendable {
        case high = "high"
        case medium = "medium"
        case low = "low"

        public var localizedTitle: String {
            switch self {
            case .high: return "高"
            case .medium: return "中"
            case .low: return "低"
            }
        }

        public var color: Color {
            switch self {
            case .high: return .red
            case .medium: return .orange
            case .low: return .green
            }
        }
    }
}

// MARK: - 配置模型
public struct ManageBacConfig: Codable, Sendable {
    public var email: String
    public var password: String
    public var schoolURL: String
    public var language: String
    public var autoRefreshInterval: Int // 分钟
    public var enableNotifications: Bool

    public init(
        email: String = "",
        password: String = "",
        schoolURL: String = "https://your-school.managebac.cn",
        language: String = "zh",
        autoRefreshInterval: Int = 30,
        enableNotifications: Bool = true
    ) {
        self.email = email
        self.password = password
        self.schoolURL = schoolURL
        self.language = language
        self.autoRefreshInterval = autoRefreshInterval
        self.enableNotifications = enableNotifications
    }

    public static let defaultConfig = ManageBacConfig()
}

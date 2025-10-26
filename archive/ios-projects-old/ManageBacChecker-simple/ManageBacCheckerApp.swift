//
//  ManageBacCheckerApp.swift
//  ManageBac Assignment Checker
//
//  Created by 方籽杰 on 2025/9/26.
//  转换自Python版本的ManageBac作业检查器
//

import SwiftUI
import UserNotifications
import ManageBacCheckerFeature

@main
struct ManageBacCheckerApp: App {
    @StateObject private var assignmentManager = AssignmentManager()

    init() {
        // 请求通知权限
        UNUserNotificationCenter.current().requestAuthorization(options: [.alert, .badge, .sound]) { granted, _ in
            print("通知权限: \(granted ? "已授权" : "被拒绝")")
        }
    }

    var body: some Scene {
        WindowGroup {
            if assignmentManager.hasCompletedOnboarding {
                    ContentView()
                        .environmentObject(assignmentManager)
            } else {
                OnboardingView()
                    .environmentObject(assignmentManager)
            }
        }
        .onChange(of: assignmentManager.hasCompletedOnboarding) { _ in
            // 当引导完成状态改变时，重新加载配置
            assignmentManager.loadConfiguration()
        }
    }
}

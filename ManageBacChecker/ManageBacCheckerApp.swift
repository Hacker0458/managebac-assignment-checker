//
//  ManageBacCheckerApp.swift
//  ManageBac Assignment Checker
//
//  Created by 方籽杰 on 2025/9/26.
//  转换自Python版本的ManageBac作业检查器
//

import SwiftUI
import UserNotifications

@main
struct ManageBacCheckerApp: App {
    @StateObject private var assignmentManager = AssignmentManager()
    @AppStorage("isOnboardingComplete") private var isOnboardingComplete = false

    var body: some Scene {
        WindowGroup {
            if isOnboardingComplete {
                ContentView()
                    .environmentObject(assignmentManager)
                    .onAppear {
                        // 应用启动时的初始化
                        Task {
                            await assignmentManager.fetchAssignments()
                        }
                    }
            } else {
                OnboardingView(isOnboardingComplete: $isOnboardingComplete)
            }
        }
    }
}


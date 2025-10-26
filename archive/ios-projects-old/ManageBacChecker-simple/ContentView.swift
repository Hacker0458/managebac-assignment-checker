//
//  ContentView.swift
//  ManageBac Assignment Checker
//
//  Created by 方籽杰 on 2025/9/26.
//  主界面视图 - 使用Swift Package
//

import SwiftUI
import ManageBacCheckerFeature

struct ContentView: View {
    @EnvironmentObject private var assignmentManager: AssignmentManager
    @State private var selectedTab = 0

    var body: some View {
        TabView(selection: $selectedTab) {
            HomeView()
                .tabItem {
                    Image(systemName: "house.fill")
                    Text("首页")
                }
                .tag(0)

            AssignmentListView()
                .tabItem {
                    Image(systemName: "list.bullet")
                    Text("作业")
                }
                .tag(1)

            StatisticsView()
                .tabItem {
                    Image(systemName: "chart.bar.fill")
                    Text("统计")
                }
                .tag(2)

            SettingsView()
                .tabItem {
                    Image(systemName: "gear")
                    Text("设置")
                }
                .tag(3)
        }
        .task {
            // 使用.task修饰符进行异步操作
            if !assignmentManager.hasCompletedOnboarding {
                assignmentManager.loadConfiguration()
            }
        }
    }
}

#Preview {
    ContentView()
        .environmentObject(AssignmentManager())
}
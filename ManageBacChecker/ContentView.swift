//
//  ContentView.swift
//  ManageBac Assignment Checker
//
//  Created by 方籽杰 on 2025/9/26.
//  主界面 - 现代化iOS作业管理界面
//

import SwiftUI

struct ContentView: View {
    @EnvironmentObject var assignmentManager: AssignmentManager
    @Environment(\.horizontalSizeClass) var horizontalSizeClass
    @State private var selectedTab = 0
    
    var body: some View {
        Group {
            if horizontalSizeClass == .compact {
                // iPhone 布局
                iPhoneLayout
            } else {
                // iPad 布局
                iPadLayout
            }
        }
        .accentColor(.blue)
    }
    
    private var iPhoneLayout: some View {
        TabView(selection: $selectedTab) {
            HomeView()
                .tabItem {
                    Image(systemName: selectedTab == 0 ? "house.fill" : "house")
                    Text("主页")
                }
                .tag(0)

            AssignmentListView()
                .tabItem {
                    Image(systemName: selectedTab == 1 ? "list.bullet.clipboard.fill" : "list.bullet.clipboard")
                    Text("作业")
                }
                .badge(assignmentManager.unsubmittedCount > 0 ? assignmentManager.unsubmittedCount : 0)
                .tag(1)

            StatisticsView()
                .tabItem {
                    Image(systemName: selectedTab == 2 ? "chart.bar.fill" : "chart.bar")
                    Text("统计")
                }
                .tag(2)

            SettingsView()
                .tabItem {
                    Image(systemName: selectedTab == 3 ? "gearshape.fill" : "gearshape")
                    Text("设置")
                }
                .tag(3)
        }
    }
    
    private var iPadLayout: some View {
        NavigationSplitView {
            // 侧边栏
            List {
                Button(action: { selectedTab = 0 }) {
                    HStack {
                        Label("主页", systemImage: "house.fill")
                        Spacer()
                        if selectedTab == 0 {
                            Image(systemName: "checkmark")
                                .foregroundColor(.blue)
                        }
                    }
                }
                .buttonStyle(.plain)
                
                Button(action: { selectedTab = 1 }) {
                    HStack {
                        Label("作业", systemImage: "list.bullet.clipboard.fill")
                        Spacer()
                        if assignmentManager.unsubmittedCount > 0 {
                            Text("\(assignmentManager.unsubmittedCount)")
                                .font(.caption)
                                .fontWeight(.semibold)
                                .foregroundColor(.white)
                                .padding(.horizontal, 8)
                                .padding(.vertical, 4)
                                .background(Color.red)
                                .clipShape(Capsule())
                        }
                        if selectedTab == 1 {
                            Image(systemName: "checkmark")
                                .foregroundColor(.blue)
                        }
                    }
                }
                .buttonStyle(.plain)
                
                Button(action: { selectedTab = 2 }) {
                    HStack {
                        Label("统计", systemImage: "chart.bar.fill")
                        Spacer()
                        if selectedTab == 2 {
                            Image(systemName: "checkmark")
                                .foregroundColor(.blue)
                        }
                    }
                }
                .buttonStyle(.plain)
                
                Button(action: { selectedTab = 3 }) {
                    HStack {
                        Label("设置", systemImage: "gearshape.fill")
                        Spacer()
                        if selectedTab == 3 {
                            Image(systemName: "checkmark")
                                .foregroundColor(.blue)
                        }
                    }
                }
                .buttonStyle(.plain)
            }
            .navigationTitle("ManageBac助手")
            .listStyle(SidebarListStyle())
            
        } detail: {
            // 详情视图
            Group {
                switch selectedTab {
                case 0:
                    HomeView()
                case 1:
                    AssignmentListView()
                case 2:
                    StatisticsView()
                case 3:
                    SettingsView()
                default:
                    HomeView()
                }
            }
        }
    }
}


#Preview {
    ContentView()
        .environmentObject(AssignmentManager())
}


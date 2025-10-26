//
//  HomeView.swift
//  ManageBacCheckerFeature
//
//  Created by AI Assistant on 2025/1/27.
//  首页视图 - 显示作业概览和快速操作
//

import SwiftUI

@MainActor
public struct HomeView: View {
    @EnvironmentObject private var assignmentManager: AssignmentManager
    @State private var showingSettings = false
    @State private var showingAddAssignment = false

    public init() {}

    public var body: some View {
        NavigationView {
            ScrollView {
                VStack(spacing: 20) {
                    // 欢迎区域
                    welcomeSection

                    // 快速统计卡片
                    quickStatsSection

                    // 即将到期的作业
                    upcomingAssignmentsSection

                    // 快速操作按钮
                    quickActionsSection

                    // 最近活动
                    recentActivitySection

                    Spacer(minLength: 20)
                }
                .padding()
            }
            .navigationTitle("ManageBac作业检查器")
            .toolbar {
                ToolbarItem(placement: .navigationBarLeading) {
                    Button(action: {
                        showingSettings = true
                    }) {
                        Image(systemName: "gearshape.fill")
                    }
                }

                ToolbarItem(placement: .navigationBarTrailing) {
                    Button(action: {
                        Task {
                            await assignmentManager.quickRefresh()
                        }
                    }) {
                        Image(systemName: "arrow.clockwise")
                    }
                    .disabled(assignmentManager.isLoading)
                }
            }
        }
        .sheet(isPresented: $showingSettings) {
            SettingsView()
        }
        .sheet(isPresented: $showingAddAssignment) {
            AddAssignmentView()
        }
        .task {
            // 使用.task修饰符进行异步操作
            if assignmentManager.assignments.isEmpty {
                await assignmentManager.refreshAssignments()
            }
        }
        .overlay {
            // 加载状态指示器
            if assignmentManager.isLoading {
                VStack {
                    Spacer()
                    HStack {
                        ProgressView()
                            .scaleEffect(0.8)
                        Text("正在加载...")
                            .font(.caption)
                            .foregroundColor(.secondary)
                    }
                    .padding()
                    .background(Color(.systemBackground))
                    .clipShape(RoundedRectangle(cornerRadius: 8))
                    .shadow(radius: 4)
                    Spacer()
                }
            }
        }
        .alert("错误", isPresented: .constant(assignmentManager.errorMessage != nil)) {
            Button("确定") {
                assignmentManager.errorMessage = nil
            }
        } message: {
            Text(assignmentManager.errorMessage ?? "")
        }
    }

    // MARK: - 欢迎区域
    private var welcomeSection: some View {
        VStack(alignment: .leading, spacing: 12) {
            HStack {
                VStack(alignment: .leading, spacing: 4) {
                    Text("欢迎回来！")
                        .font(.title2)
                        .fontWeight(.bold)
                    Text("今天有 \(assignmentManager.assignmentsDueToday.count) 个作业即将到期")
                        .font(.subheadline)
                        .foregroundColor(.secondary)
                }
                Spacer()
                Image(systemName: "person.circle.fill")
                    .font(.system(size: 40))
                    .foregroundColor(.blue)
            }
        }
        .padding()
        .background(Color(.systemGray6))
        .clipShape(RoundedRectangle(cornerRadius: 12))
    }

    // MARK: - 快速统计
    private var quickStatsSection: some View {
        LazyVGrid(columns: [
            GridItem(.flexible()),
            GridItem(.flexible())
        ], spacing: 16) {
            StatCard(
                title: "总作业数",
                value: "\(assignmentManager.assignments.count)",
                icon: "doc.text.fill",
                color: .blue
            )

            StatCard(
                title: "待完成",
                value: "\(assignmentManager.pendingAssignments.count)",
                icon: "clock.fill",
                color: .orange
            )

            StatCard(
                title: "已完成",
                value: "\(assignmentManager.completedAssignments.count)",
                icon: "checkmark.circle.fill",
                color: .green
            )

            StatCard(
                title: "已逾期",
                value: "\(assignmentManager.overdueAssignments.count)",
                icon: "exclamationmark.triangle.fill",
                color: .red
            )
        }
    }

    // MARK: - 即将到期的作业
    private var upcomingAssignmentsSection: some View {
        VStack(alignment: .leading, spacing: 12) {
            HStack {
                Text("即将到期")
                    .font(.headline)
                    .fontWeight(.semibold)
                Spacer()
                NavigationLink("查看全部") {
                    AssignmentListView()
                }
                .font(.subheadline)
                .foregroundColor(.blue)
            }

            if assignmentManager.assignmentsDueToday.isEmpty {
                VStack(spacing: 8) {
                    Image(systemName: "checkmark.circle.fill")
                        .font(.system(size: 30))
                        .foregroundColor(.green)
                    Text("今天没有即将到期的作业")
                        .font(.subheadline)
                        .foregroundColor(.secondary)
                }
                .frame(maxWidth: .infinity)
                .padding(.vertical, 20)
            } else {
                LazyVStack(spacing: 8) {
                    ForEach(assignmentManager.assignmentsDueToday.prefix(3)) { assignment in
                        AssignmentRowView(assignment: assignment)
                    }
                }
            }
        }
        .padding()
        .background(Color(.systemBackground))
        .clipShape(RoundedRectangle(cornerRadius: 12))
        .shadow(color: .black.opacity(0.05), radius: 2, x: 0, y: 1)
    }

    // MARK: - 快速操作
    private var quickActionsSection: some View {
        VStack(alignment: .leading, spacing: 12) {
            Text("快速操作")
                .font(.headline)
                .fontWeight(.semibold)

            LazyVGrid(columns: [
                GridItem(.flexible()),
                GridItem(.flexible())
            ], spacing: 12) {
                QuickActionButton(
                    title: "添加作业",
                    icon: "plus.circle.fill",
                    color: .blue
                ) {
                    showingAddAssignment = true
                }

                QuickActionButton(
                    title: "同步数据",
                    icon: "arrow.clockwise.circle.fill",
                    color: .green
                ) {
                    Task {
                        await assignmentManager.quickRefresh()
                    }
                }

                QuickActionButton(
                    title: "查看统计",
                    icon: "chart.bar.fill",
                    color: .purple
                ) {
                    // 导航到统计页面
                }

                QuickActionButton(
                    title: "设置提醒",
                    icon: "bell.fill",
                    color: .orange
                ) {
                    // 打开提醒设置
                }
            }
        }
        .padding()
        .background(Color(.systemBackground))
        .clipShape(RoundedRectangle(cornerRadius: 12))
        .shadow(color: .black.opacity(0.05), radius: 2, x: 0, y: 1)
    }

    // MARK: - 最近活动
    private var recentActivitySection: some View {
        VStack(alignment: .leading, spacing: 12) {
            Text("最近活动")
                .font(.headline)
                .fontWeight(.semibold)

            VStack(spacing: 8) {
                ActivityRow(
                    icon: "arrow.clockwise.circle.fill",
                    title: "数据同步完成",
                    subtitle: "刚刚",
                    color: .green
                )

                ActivityRow(
                    icon: "checkmark.circle.fill",
                    title: "完成数学作业",
                    subtitle: "2小时前",
                    color: .blue
                )

                ActivityRow(
                    icon: "bell.fill",
                    title: "提醒设置成功",
                    subtitle: "昨天",
                    color: .orange
                )
            }
        }
        .padding()
        .background(Color(.systemBackground))
        .clipShape(RoundedRectangle(cornerRadius: 12))
        .shadow(color: .black.opacity(0.05), radius: 2, x: 0, y: 1)
    }
}

// MARK: - 统计卡片
@MainActor
public struct StatCard: View {
    let title: String
    let value: String
    let icon: String
    let color: Color

    public init(title: String, value: String, icon: String, color: Color) {
        self.title = title
        self.value = value
        self.icon = icon
        self.color = color
    }

    public var body: some View {
        VStack(spacing: 8) {
            Image(systemName: icon)
                .font(.system(size: 24))
                .foregroundColor(color)

            Text(value)
                .font(.title2)
                .fontWeight(.bold)
                .foregroundColor(.primary)

            Text(title)
                .font(.caption)
                .foregroundColor(.secondary)
        }
        .frame(maxWidth: .infinity)
        .padding()
        .background(Color(.systemGray6))
        .clipShape(RoundedRectangle(cornerRadius: 12))
    }
}

// MARK: - 作业行视图
@MainActor
public struct AssignmentRowView: View {
    let assignment: Assignment

    public init(assignment: Assignment) {
        self.assignment = assignment
    }

    public var body: some View {
        HStack(spacing: 12) {
            // 状态指示器
            Circle()
                .fill(assignment.status.color)
                .frame(width: 8, height: 8)

            VStack(alignment: .leading, spacing: 2) {
                Text(assignment.title)
                    .font(.subheadline)
                    .fontWeight(.medium)
                    .lineLimit(1)

                Text(assignment.subject)
                    .font(.caption)
                    .foregroundColor(.secondary)
            }

            Spacer()

            if let dueDate = assignment.dueDate {
                VStack(alignment: .trailing, spacing: 2) {
                    Text(dueDate, style: .time)
                        .font(.caption)
                        .fontWeight(.medium)
                    Text(dueDate, style: .date)
                        .font(.caption2)
                        .foregroundColor(.secondary)
                }
            }
        }
        .padding(.vertical, 4)
    }
}

// MARK: - 快速操作按钮
@MainActor
public struct QuickActionButton: View {
    let title: String
    let icon: String
    let color: Color
    let action: () -> Void

    public init(title: String, icon: String, color: Color, action: @escaping () -> Void) {
        self.title = title
        self.icon = icon
        self.color = color
        self.action = action
    }

    public var body: some View {
        Button(action: action) {
            VStack(spacing: 8) {
                Image(systemName: icon)
                    .font(.system(size: 24))
                    .foregroundColor(color)

                Text(title)
                    .font(.caption)
                    .fontWeight(.medium)
                    .foregroundColor(.primary)
            }
            .frame(maxWidth: .infinity)
            .padding()
            .background(Color(.systemGray6))
            .clipShape(RoundedRectangle(cornerRadius: 12))
        }
        .buttonStyle(PlainButtonStyle())
    }
}

// MARK: - 活动行
@MainActor
public struct ActivityRow: View {
    let icon: String
    let title: String
    let subtitle: String
    let color: Color

    public init(icon: String, title: String, subtitle: String, color: Color) {
        self.icon = icon
        self.title = title
        self.subtitle = subtitle
        self.color = color
    }

    public var body: some View {
        HStack(spacing: 12) {
            Image(systemName: icon)
                .font(.system(size: 16))
                .foregroundColor(color)
                .frame(width: 20)

            VStack(alignment: .leading, spacing: 2) {
                Text(title)
                    .font(.subheadline)
                    .fontWeight(.medium)

                Text(subtitle)
                    .font(.caption)
                    .foregroundColor(.secondary)
            }

            Spacer()
        }
        .padding(.vertical, 4)
    }
}

#Preview {
    HomeView()
        .environmentObject(AssignmentManager())
}

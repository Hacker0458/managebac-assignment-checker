//
//  HomeView.swift
//  ManageBac Assignment Checker
//
//  Created by 方籽杰 on 2025/9/27.
//  主页视图 - 显示作业概览和快速统计
//

import SwiftUI

struct HomeView: View {
    @EnvironmentObject var assignmentManager: AssignmentManager

    var body: some View {
        NavigationView {
            ScrollView {
                VStack(spacing: 24) {
                    // 欢迎标题
                    welcomeHeader

                    // 快速统计卡片
                    quickStatsSection

                    // 即将到期的作业
                    upcomingAssignmentsSection

                    // 最近活动
                    recentActivitySection

                    Spacer(minLength: 20)
                }
                .padding()
            }
            .navigationTitle("ManageBac作业检查器")
            .navigationBarTitleDisplayMode(.large)
            .refreshable {
                await assignmentManager.fetchAssignments()
            }
            .overlay {
                if assignmentManager.isLoading {
                    LoadingOverlay()
                }
            }
        }
    }

    private var welcomeHeader: some View {
        VStack(spacing: 16) {
            // 动态问候语
            HStack {
                VStack(alignment: .leading, spacing: 4) {
                    Text(getGreeting())
                        .font(.title2)
                        .fontWeight(.medium)
                        .foregroundColor(.secondary)
                    
                    Text("今天有什么计划？")
                        .font(.largeTitle)
                        .fontWeight(.bold)
                        .foregroundStyle(
                            LinearGradient(
                                colors: [.blue, .purple],
                                startPoint: .leading,
                                endPoint: .trailing
                            )
                        )
                }
                
                Spacer()
                
                // 用户头像占位符
                Circle()
                    .fill(
                        LinearGradient(
                            colors: [.blue.opacity(0.3), .purple.opacity(0.3)],
                            startPoint: .topLeading,
                            endPoint: .bottomTrailing
                        )
                    )
                    .frame(width: 50, height: 50)
                    .overlay(
                        Image(systemName: "person.fill")
                            .foregroundColor(.white)
                            .font(.title2)
                    )
            }
            
            // 快速状态指示器
            if assignmentManager.isLoggedIn {
                HStack(spacing: 4) {
                    Image(systemName: "checkmark.circle.fill")
                        .foregroundColor(.green)
                    Text("已连接到 ManageBac")
                        .font(.caption)
                        .foregroundColor(.secondary)
                }
            } else {
                HStack(spacing: 4) {
                    Image(systemName: "exclamationmark.triangle.fill")
                        .foregroundColor(.orange)
                    Text("未连接到 ManageBac")
                        .font(.caption)
                        .foregroundColor(.secondary)
                }
            }
        }
        .padding(.horizontal)
        .padding(.top, 10)
    }
    
    private func getGreeting() -> String {
        let hour = Calendar.current.component(.hour, from: Date())
        switch hour {
        case 6..<12:
            return "早上好"
        case 12..<18:
            return "下午好"
        case 18..<22:
            return "晚上好"
        default:
            return "夜深了"
        }
    }

    private var quickStatsSection: some View {
        VStack(alignment: .leading, spacing: 16) {
            Text("快速统计")
                .font(.headline)
                .fontWeight(.semibold)

            LazyVGrid(columns: [
                GridItem(.flexible()),
                GridItem(.flexible())
            ], spacing: 16) {
                SimpleStatCard(
                    title: "作业总数",
                    value: "\(assignmentManager.assignments.count)",
                    icon: "doc.text",
                    color: .blue
                )

                SimpleStatCard(
                    title: "未提交",
                    value: "\(assignmentManager.unsubmittedCount)",
                    icon: "exclamationmark.triangle",
                    color: .red
                )

                SimpleStatCard(
                    title: "逾期",
                    value: "\(assignmentManager.overdueCount)",
                    icon: "clock.badge.exclamationmark",
                    color: .orange
                )

                SimpleStatCard(
                    title: "高优先级",
                    value: "\(assignmentManager.highPriorityCount)",
                    icon: "flag.fill",
                    color: .purple
                )
            }
        }
    }

    private var upcomingAssignmentsSection: some View {
        VStack(alignment: .leading, spacing: 16) {
            HStack {
                Text("即将到期")
                    .font(.headline)
                    .fontWeight(.semibold)
                Spacer()
            }

            let upcomingAssignments = assignmentManager.assignmentsDueSoon().prefix(3)

            if upcomingAssignments.isEmpty {
                SimpleEmptyStateView(
                    icon: "checkmark.circle.fill",
                    title: "太棒了！",
                    subtitle: "暂无即将到期的作业",
                    color: .green
                )
            } else {
                LazyVStack(spacing: 12) {
                    ForEach(Array(upcomingAssignments), id: \.id) { assignment in
                        SimpleAssignmentCard(assignment: assignment)
                    }
                }
            }
        }
    }

    private var recentActivitySection: some View {
        VStack(alignment: .leading, spacing: 16) {
            Text("最近活动")
                .font(.headline)
                .fontWeight(.semibold)

            if let lastUpdateTime = assignmentManager.lastUpdateTime {
                HStack {
                    Image(systemName: "clock")
                        .foregroundColor(.secondary)
                    Text("最后更新: \(lastUpdateTime.formatted(.dateTime.hour().minute()))")
                        .font(.caption)
                        .foregroundColor(.secondary)
                    Spacer()
                }
            }

            if assignmentManager.isLoading {
                HStack {
                    ProgressView()
                        .scaleEffect(0.8)
                    Text("正在获取作业数据...")
                        .font(.caption)
                        .foregroundColor(.secondary)
                }
            }
        }
    }
}

// MARK: - 简化的统计卡片组件
struct SimpleStatCard: View {
    let title: String
    let value: String
    let icon: String
    let color: Color

    var body: some View {
        VStack(spacing: 8) {
            HStack {
                Image(systemName: icon)
                    .foregroundColor(color)
                    .font(.title2)
                Spacer()
            }

            VStack(alignment: .leading, spacing: 2) {
                Text(value)
                    .font(.title)
                    .fontWeight(.bold)
                    .foregroundColor(.primary)

                Text(title)
                    .font(.caption)
                    .foregroundColor(.secondary)
                    .lineLimit(2)
            }
            .frame(maxWidth: .infinity, alignment: .leading)
        }
        .padding()
        .background(Color(.systemBackground))
        .cornerRadius(12)
        .shadow(color: .black.opacity(0.05), radius: 5, x: 0, y: 2)
    }
}

// MARK: - 简化的作业卡片
struct SimpleAssignmentCard: View {
    let assignment: Assignment

    var body: some View {
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
                    Text(dueDate, style: .relative)
                        .font(.caption)
                        .fontWeight(.medium)
                        .foregroundColor(timeRemainingColor(for: dueDate))

                    Text(dueDate, style: .date)
                        .font(.caption2)
                        .foregroundColor(.secondary)
                }
            }
        }
        .padding(.horizontal, 16)
        .padding(.vertical, 12)
        .background(Color(.secondarySystemBackground))
        .cornerRadius(10)
    }

    private func timeRemainingColor(for date: Date) -> Color {
        let timeInterval = date.timeIntervalSinceNow
        let hoursLeft = timeInterval / 3600

        if hoursLeft < 24 {
            return .red
        } else if hoursLeft < 72 {
            return .orange
        } else {
            return .primary
        }
    }
}

// MARK: - 简化的空状态视图
struct SimpleEmptyStateView: View {
    let icon: String
    let title: String
    let subtitle: String
    let color: Color

    var body: some View {
        VStack(spacing: 16) {
            Image(systemName: icon)
                .font(.system(size: 48))
                .foregroundColor(color)

            VStack(spacing: 4) {
                Text(title)
                    .font(.headline)
                    .fontWeight(.semibold)

                Text(subtitle)
                    .font(.subheadline)
                    .foregroundColor(.secondary)
                    .multilineTextAlignment(.center)
            }
        }
        .padding(.vertical, 32)
        .frame(maxWidth: .infinity)
    }
}

#if DEBUG
struct HomeView_Previews: PreviewProvider {
    static var previews: some View {
        HomeView()
            .environmentObject(AssignmentManager())
    }
}
#endif

// MARK: - 加载覆盖层
struct LoadingOverlay: View {
    var body: some View {
        ZStack {
            Color.black.opacity(0.3)
                .ignoresSafeArea()
            
            VStack(spacing: 16) {
                ProgressView()
                    .scaleEffect(1.2)
                    .progressViewStyle(CircularProgressViewStyle(tint: .white))
                
                Text("正在获取作业数据...")
                    .font(.subheadline)
                    .foregroundColor(.white)
                    .multilineTextAlignment(.center)
            }
            .padding(24)
            .background(
                RoundedRectangle(cornerRadius: 16)
                    .fill(.regularMaterial)
            )
            .shadow(radius: 10)
        }
    }
}

#Preview("Loading") {
    ZStack {
        Color.gray.opacity(0.1)
            .ignoresSafeArea()
        LoadingOverlay()
    }
}
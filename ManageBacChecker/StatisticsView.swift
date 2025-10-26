//
//  StatisticsView.swift
//  ManageBac Assignment Checker
//
//  Created by 方籽杰 on 2025/9/26.
//  统计视图 - 显示作业数据分析和图表
//

import SwiftUI
// import Charts - Using native SwiftUI components instead

struct StatisticsView: View {
    @EnvironmentObject var assignmentManager: AssignmentManager

    var body: some View {
        NavigationView {
            ScrollView {
                VStack(spacing: 20) {
                    // 总体统计卡片
                    overviewCards

                    // 状态分布图表
                    statusDistributionChart

                    // 学科分布图表
                    subjectDistributionChart

                    // 本周作业趋势
                    weeklyTrendChart

                    // 优先级分析
                    priorityAnalysis

                    Spacer(minLength: 20)
                }
                .padding()
            }
            .navigationTitle("统计分析")
            .refreshable {
                await assignmentManager.fetchAssignments()
            }
        }
    }

    private var overviewCards: some View {
        LazyVGrid(columns: [
            GridItem(.flexible()),
            GridItem(.flexible())
        ], spacing: 15) {
            OverviewCard(
                title: "完成率",
                value: completionRate,
                subtitle: "已提交/总数",
                color: .green,
                icon: "chart.pie.fill"
            )

            OverviewCard(
                title: "平均剩余时间",
                value: averageTimeRemaining,
                subtitle: "到截止日期",
                color: .blue,
                icon: "clock.fill"
            )

            OverviewCard(
                title: "逾期率",
                value: overdueRate,
                subtitle: "需要关注",
                color: .red,
                icon: "exclamationmark.triangle.fill"
            )

            OverviewCard(
                title: "高优先级",
                value: "\(assignmentManager.highPriorityCount)",
                subtitle: "重点作业",
                color: .purple,
                icon: "star.fill"
            )
        }
    }

    private var statusDistributionChart: some View {
        VStack(alignment: .leading, spacing: 12) {
            Text("作业状态分布")
                .font(.headline)
                .fontWeight(.semibold)

            // iOS 15 兼容版本 - 使用简单的进度条
            VStack(spacing: 8) {
                ForEach(statusData, id: \.status) { data in
                    HStack {
                        Circle()
                            .fill(data.color)
                            .frame(width: 8, height: 8)
                        Text(data.status.localizedTitle)
                            .font(.subheadline)
                        Spacer()
                        Text("\(data.count)")
                            .font(.subheadline)
                            .fontWeight(.medium)
                    }
                }
            }
            .padding()
            .background(Color(UIColor.systemGray6))
            .clipShape(RoundedRectangle(cornerRadius: 10))

            // 图例
            LazyVGrid(columns: [
                GridItem(.flexible()),
                GridItem(.flexible())
            ], spacing: 8) {
                ForEach(statusData, id: \.status) { data in
                    HStack(spacing: 6) {
                        Circle()
                            .fill(data.color)
                            .frame(width: 8, height: 8)
                        Text(data.status.localizedTitle)
                            .font(.caption)
                        Spacer()
                        Text("\(data.count)")
                            .font(.caption)
                            .fontWeight(.medium)
                    }
                }
            }
        }
        .padding()
        .background(Color(UIColor.secondarySystemBackground))
        .clipShape(RoundedRectangle(cornerRadius: 12))
    }

    private var subjectDistributionChart: some View {
        VStack(alignment: .leading, spacing: 12) {
            Text("学科分布")
                .font(.headline)
                .fontWeight(.semibold)

            // iOS 15 兼容版本
            VStack(spacing: 8) {
                ForEach(subjectData, id: \.subject) { data in
                    HStack {
                        Text(data.subject)
                            .font(.subheadline)
                            .frame(width: 80, alignment: .leading)

                        GeometryReader { geometry in
                            HStack(spacing: 0) {
                                Rectangle()
                                    .fill(Color.blue)
                                    .frame(width: geometry.size.width * CGFloat(data.count) / CGFloat(maxSubjectCount))
                                    .clipShape(RoundedRectangle(cornerRadius: 4))

                                Spacer()
                            }
                        }
                        .frame(height: 20)

                        Text("\(data.count)")
                            .font(.subheadline)
                            .fontWeight(.medium)
                            .frame(width: 30, alignment: .trailing)
                    }
                }
            }
            .padding()
            .background(Color(UIColor.systemGray6))
            .clipShape(RoundedRectangle(cornerRadius: 10))
        }
        .padding()
        .background(Color(UIColor.secondarySystemBackground))
        .clipShape(RoundedRectangle(cornerRadius: 12))
    }

    private var weeklyTrendChart: some View {
        VStack(alignment: .leading, spacing: 12) {
            Text("本周作业截止趋势")
                .font(.headline)
                .fontWeight(.semibold)

            // iOS 15 兼容版本
            Text("需要 iOS 16+ 显示图表")
                .font(.caption)
                .foregroundColor(.secondary)
                .padding()
                .frame(maxWidth: .infinity)
                .background(Color(UIColor.systemGray6))
                .clipShape(RoundedRectangle(cornerRadius: 10))
        }
        .padding()
        .background(Color(UIColor.secondarySystemBackground))
        .clipShape(RoundedRectangle(cornerRadius: 12))
    }

    private var priorityAnalysis: some View {
        VStack(alignment: .leading, spacing: 12) {
            Text("优先级分析")
                .font(.headline)
                .fontWeight(.semibold)

            LazyVGrid(columns: [
                GridItem(.flexible()),
                GridItem(.flexible()),
                GridItem(.flexible())
            ], spacing: 12) {
                ForEach(priorityData, id: \.priority) { data in
                    VStack(spacing: 8) {
                        Circle()
                            .fill(data.color.opacity(0.2))
                            .frame(width: 50, height: 50)
                            .overlay(
                                Text("\(data.count)")
                                    .font(.title2)
                                    .fontWeight(.bold)
                                    .foregroundColor(data.color)
                            )

                        Text(data.priority.localizedTitle)
                            .font(.caption)
                            .fontWeight(.medium)
                    }
                    .padding()
                    .background(Color(UIColor.systemGray6))
                    .clipShape(RoundedRectangle(cornerRadius: 10))
                }
            }
        }
        .padding()
        .background(Color(UIColor.secondarySystemBackground))
        .clipShape(RoundedRectangle(cornerRadius: 12))
    }

    // MARK: - 计算属性
    private var completionRate: String {
        let total = assignmentManager.assignments.count
        guard total > 0 else { return "0%" }

        let completed = assignmentManager.assignments.filter {
            $0.status == .submitted || $0.status == .graded
        }.count

        let rate = Double(completed) / Double(total) * 100
        return String(format: "%.0f%%", rate)
    }

    private var overdueRate: String {
        let total = assignmentManager.assignments.count
        guard total > 0 else { return "0%" }

        let overdue = assignmentManager.overdueCount
        let rate = Double(overdue) / Double(total) * 100
        return String(format: "%.0f%%", rate)
    }

    private var averageTimeRemaining: String {
        let unsubmitted = assignmentManager.assignments.filter {
            $0.status == .notSubmitted && $0.dueDate != nil
        }

        guard !unsubmitted.isEmpty else { return "N/A" }

        let now = Date()
        let totalHours = unsubmitted.compactMap { assignment in
            guard let dueDate = assignment.dueDate else { return nil }
            return max(0, dueDate.timeIntervalSince(now) / 3600)
        }.reduce(0.0) { $0 + $1 }

        let averageHours = totalHours / Double(unsubmitted.count)

        if averageHours < 24 {
            return String(format: "%.0f小时", averageHours)
        } else {
            return String(format: "%.1f天", averageHours / 24)
        }
    }

    private var statusData: [(status: Assignment.AssignmentStatus, count: Int, color: Color)] {
        Assignment.AssignmentStatus.allCases.map { status in
            let count = assignmentManager.assignments.filter { $0.status == status }.count
            return (status: status, count: count, color: status.color)
        }.filter { $0.count > 0 }
    }

    private var subjectData: [(subject: String, count: Int)] {
        let subjectCounts = Dictionary(grouping: assignmentManager.assignments, by: \.subject)
            .mapValues { $0.count }

        return subjectCounts.map { (subject: $0.key, count: $0.value) }
            .sorted { $0.count > $1.count }
    }

    private var maxSubjectCount: Int {
        subjectData.map(\.count).max() ?? 1
    }

    private var priorityData: [(priority: Assignment.Priority, count: Int, color: Color)] {
        Assignment.Priority.allCases.map { priority in
            let count = assignmentManager.assignments.filter { $0.priority == priority }.count
            return (priority: priority, count: count, color: priority.color)
        }
    }

    private var weeklyData: [(day: String, count: Int)] {
        let calendar = Calendar.current
        let today = Date()
        let days = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]

        return (0..<7).map { offset in
            let date = calendar.date(byAdding: .day, value: offset, to: today)!
            let dayOfWeek = calendar.component(.weekday, from: date)
            let dayName = days[(dayOfWeek + 5) % 7] // 调整为周一开始

            let count = assignmentManager.assignments.filter { assignment in
                guard let dueDate = assignment.dueDate else { return false }
                return calendar.isDate(dueDate, inSameDayAs: date)
            }.count

            return (day: dayName, count: count)
        }
    }
}

// MARK: - 概览卡片组件
struct OverviewCard: View {
    let title: String
    let value: String
    let subtitle: String
    let color: Color
    let icon: String

    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            HStack {
                Image(systemName: icon)
                    .font(.system(size: 16, weight: .semibold))
                    .foregroundColor(color)
                Spacer()
            }

            VStack(alignment: .leading, spacing: 2) {
                Text(value)
                    .font(.title)
                    .fontWeight(.bold)
                    .foregroundColor(color)

                Text(title)
                    .font(.headline)
                    .fontWeight(.medium)

                Text(subtitle)
                    .font(.caption)
                    .foregroundColor(.secondary)
            }
        }
        .padding()
        .background(color.opacity(0.1))
        .clipShape(RoundedRectangle(cornerRadius: 12))
    }
}

#Preview {
    StatisticsView()
        .environmentObject(AssignmentManager())
}


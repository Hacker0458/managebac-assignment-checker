//
//  AssignmentListView.swift
//  ManageBac Assignment Checker
//
//  Created by 方籽杰 on 2025/9/26.
//  作业列表视图 - 详细的作业管理界面
//

import SwiftUI

struct AssignmentListView: View {
    @EnvironmentObject var assignmentManager: AssignmentManager
    @State private var searchText = ""
    @State private var selectedFilter: AssignmentFilter = .all
    @State private var showingFilterSheet = false

    enum AssignmentFilter: String, CaseIterable {
        case all = "all"
        case notSubmitted = "notSubmitted"
        case submitted = "submitted"
        case late = "late"
        case graded = "graded"
        case highPriority = "highPriority"

        var localizedTitle: String {
            switch self {
            case .all: return "全部"
            case .notSubmitted: return "未提交"
            case .submitted: return "已提交"
            case .late: return "逾期"
            case .graded: return "已评分"
            case .highPriority: return "高优先级"
            }
        }

        func filter(_ assignments: [Assignment]) -> [Assignment] {
            switch self {
            case .all:
                return assignments
            case .notSubmitted:
                return assignments.filter { $0.status == .notSubmitted }
            case .submitted:
                return assignments.filter { $0.status == .submitted }
            case .late:
                return assignments.filter { $0.status == .late }
            case .graded:
                return assignments.filter { $0.status == .graded }
            case .highPriority:
                return assignments.filter { $0.priority == .high }
            }
        }
    }

    var filteredAssignments: [Assignment] {
        let filtered = selectedFilter.filter(assignmentManager.assignments)

        if searchText.isEmpty {
            return filtered.sorted { assignment1, assignment2 in
                // 优先级排序：未提交 > 逾期 > 其他
                let priority1 = priorityValue(for: assignment1.status)
                let priority2 = priorityValue(for: assignment2.status)

                if priority1 != priority2 {
                    return priority1 > priority2
                }

                // 按截止日期排序
                guard let date1 = assignment1.dueDate, let date2 = assignment2.dueDate else {
                    return assignment1.dueDate != nil
                }
                return date1 < date2
            }
        } else {
            return filtered.filter { assignment in
                assignment.title.localizedCaseInsensitiveContains(searchText) ||
                assignment.subject.localizedCaseInsensitiveContains(searchText) ||
                assignment.description.localizedCaseInsensitiveContains(searchText)
            }
        }
    }

    private func priorityValue(for status: Assignment.AssignmentStatus) -> Int {
        switch status {
        case .late: return 3
        case .notSubmitted: return 2
        case .submitted: return 1
        case .graded: return 0
        }
    }

    var body: some View {
        NavigationView {
            VStack(spacing: 0) {
                // 搜索和筛选栏
                VStack(spacing: 12) {
                    // 搜索框
                    HStack {
                        Image(systemName: "magnifyingglass")
                            .foregroundColor(.secondary)

                        TextField("搜索作业...", text: $searchText)
                            .textFieldStyle(PlainTextFieldStyle())

                        if !searchText.isEmpty {
                            Button {
                                searchText = ""
                            } label: {
                                Image(systemName: "xmark.circle.fill")
                                    .foregroundColor(.secondary)
                            }
                        }
                    }
                    .padding(.horizontal, 12)
                    .padding(.vertical, 8)
                    .background(Color(UIColor.systemGray6))
                    .clipShape(RoundedRectangle(cornerRadius: 10))

                    // 筛选器
                    ScrollView(.horizontal, showsIndicators: false) {
                        HStack(spacing: 8) {
                            ForEach(AssignmentFilter.allCases, id: \.self) { filter in
                                FilterChip(
                                    title: filter.rawValue,
                                    isSelected: selectedFilter == filter,
                                    count: filter.filter(assignmentManager.assignments).count
                                ) {
                                    selectedFilter = filter
                                }
                            }
                        }
                        .padding(.horizontal)
                    }
                }
                .padding(.top)
                .background(Color(UIColor.systemBackground))

                // 作业列表
                if filteredAssignments.isEmpty {
                    emptyState
                } else {
                    List {
                        ForEach(filteredAssignments) { assignment in
                            SimpleAssignmentRowView(assignment: assignment)
                                .listRowSeparator(.hidden)
                                .listRowBackground(Color.clear)
                        }
                    }
                    .listStyle(PlainListStyle())
                    .refreshable {
                        await assignmentManager.fetchAssignments()
                    }
                }
            }
            .navigationTitle("作业列表")
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button {
                        Task {
                            await assignmentManager.fetchAssignments()
                        }
                    } label: {
                        Image(systemName: "arrow.clockwise")
                    }
                    .disabled(assignmentManager.isLoading)
                }
            }
        }
    }

    private var emptyState: some View {
        VStack(spacing: 16) {
            Spacer()

            Image(systemName: selectedFilter == .all ? "list.bullet.clipboard" : "magnifyingglass")
                .font(.system(size: 50))
                .foregroundColor(.secondary)

            Text(emptyStateMessage)
                .font(.headline)
                .multilineTextAlignment(.center)
                .foregroundColor(.secondary)

            if selectedFilter != .all || !searchText.isEmpty {
                Button("清除筛选") {
                    selectedFilter = .all
                    searchText = ""
                }
                .buttonStyle(.bordered)
            }

            Spacer()
        }
        .padding()
    }

    private var emptyStateMessage: String {
        if !searchText.isEmpty {
            return "没有找到匹配 \"\(searchText)\" 的作业"
        } else {
            switch selectedFilter {
            case .all:
                return "暂无作业数据\n请点击刷新按钮同步作业"
            case .notSubmitted:
                return "太棒了！\n没有未提交的作业 🎉"
            case .late:
                return "很好！\n没有逾期的作业"
            case .submitted:
                return "还没有已提交的作业"
            case .graded:
                return "还没有已评分的作业"
            case .highPriority:
                return "没有高优先级的作业"
            }
        }
    }
}

// MARK: - 筛选器芯片组件
struct FilterChip: View {
    let title: String
    let isSelected: Bool
    let count: Int
    let action: () -> Void

    var body: some View {
        Button(action: action) {
            HStack(spacing: 4) {
                Text(title)
                    .font(.caption)
                    .fontWeight(isSelected ? .semibold : .medium)

                if count > 0 {
                    Text("\(count)")
                        .font(.caption2)
                        .fontWeight(.semibold)
                        .padding(.horizontal, 6)
                        .padding(.vertical, 2)
                        .background(isSelected ? Color.white : Color.primary.opacity(0.2))
                        .clipShape(Capsule())
                }
            }
            .padding(.horizontal, 12)
            .padding(.vertical, 6)
            .background(isSelected ? Color.blue : Color(UIColor.systemGray5))
            .foregroundColor(isSelected ? .white : .primary)
            .clipShape(Capsule())
        }
        .buttonStyle(PlainButtonStyle())
    }
}

// MARK: - 简化的作业行视图
struct SimpleAssignmentRowView: View {
    let assignment: Assignment

    var body: some View {
        HStack(spacing: 12) {
            // 状态图标
            ZStack {
                Circle()
                    .fill(assignment.status.color.opacity(0.2))
                    .frame(width: 40, height: 40)

                Image(systemName: assignment.status.icon)
                    .font(.system(size: 16, weight: .medium))
                    .foregroundColor(assignment.status.color)
            }

            VStack(alignment: .leading, spacing: 4) {
                Text(assignment.title)
                    .font(.headline)
                    .fontWeight(.medium)
                    .lineLimit(2)

                Text(assignment.subject)
                    .font(.caption)
                    .foregroundColor(.secondary)

                if let dueDate = assignment.dueDate {
                    HStack(spacing: 4) {
                        Image(systemName: "clock")
                            .font(.system(size: 10))
                        Text(dueDate.formatted(.dateTime.month().day().hour().minute()))
                            .font(.caption)
                    }
                    .foregroundColor(dueDate < Date() ? .red : .secondary)
                }
            }

            Spacer()

            // 优先级指示器
            VStack {
                Circle()
                    .fill(assignment.priority.color)
                    .frame(width: 8, height: 8)

                Text(assignment.priority.localizedTitle)
                    .font(.caption2)
                    .foregroundColor(assignment.priority.color)
            }
        }
        .padding(12)
        .background(Color(UIColor.secondarySystemBackground))
        .clipShape(RoundedRectangle(cornerRadius: 8))
    }
}

// MARK: - 作业详情视图
struct AssignmentDetailView: View {
    let assignment: Assignment
    @Environment(\.dismiss) private var dismiss

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 20) {
                // 头部信息
                VStack(alignment: .leading, spacing: 12) {
                    HStack {
                        VStack(alignment: .leading, spacing: 4) {
                            Text(assignment.title)
                                .font(.title2)
                                .fontWeight(.bold)

                            Text(assignment.subject)
                                .font(.headline)
                                .foregroundColor(.secondary)
                        }

                        Spacer()

                        VStack(spacing: 4) {
                            ZStack {
                                Circle()
                                    .fill(assignment.status.color.opacity(0.2))
                                    .frame(width: 50, height: 50)

                                Image(systemName: assignment.status.icon)
                                    .font(.system(size: 20, weight: .medium))
                                    .foregroundColor(assignment.status.color)
                            }

                            Text(assignment.status.localizedTitle)
                                .font(.caption)
                                .fontWeight(.medium)
                                .foregroundColor(assignment.status.color)
                        }
                    }

                    // 优先级和截止日期
                    HStack(spacing: 16) {
                        Label(assignment.priority.localizedTitle, systemImage: "star.fill")
                            .foregroundColor(assignment.priority.color)
                            .font(.subheadline)
                            .fontWeight(.medium)

                        if let dueDate = assignment.dueDate {
                            Label(
                                dueDate.formatted(.dateTime.weekday().month().day().hour().minute()),
                                systemImage: "calendar"
                            )
                            .foregroundColor(dueDate < Date() ? .red : .secondary)
                            .font(.subheadline)
                        }
                    }
                }
                .padding()
                .background(Color(UIColor.secondarySystemBackground))
                .clipShape(RoundedRectangle(cornerRadius: 12))

                // 作业描述
                VStack(alignment: .leading, spacing: 8) {
                    Text("作业描述")
                        .font(.headline)
                        .fontWeight(.semibold)

                    Text(assignment.description)
                        .font(.body)
                        .foregroundColor(.secondary)
                }
                .padding()
                .background(Color(UIColor.secondarySystemBackground))
                .clipShape(RoundedRectangle(cornerRadius: 12))

                // 快速操作
                if assignment.status == .notSubmitted {
                    VStack(spacing: 12) {
                        Text("快速操作")
                            .font(.headline)
                            .fontWeight(.semibold)

                        VStack(spacing: 8) {
                            Button {
                                // TODO: 标记为已提交
                            } label: {
                                Label("标记为已提交", systemImage: "checkmark.circle")
                                    .frame(maxWidth: .infinity)
                                    .padding()
                                    .background(Color.green)
                                    .foregroundColor(.white)
                                    .clipShape(RoundedRectangle(cornerRadius: 10))
                            }

                            Button {
                                // TODO: 设置提醒
                            } label: {
                                Label("设置提醒", systemImage: "bell")
                                    .frame(maxWidth: .infinity)
                                    .padding()
                                    .background(Color.blue)
                                    .foregroundColor(.white)
                                    .clipShape(RoundedRectangle(cornerRadius: 10))
                            }
                        }
                    }
                    .padding()
                    .background(Color(UIColor.secondarySystemBackground))
                    .clipShape(RoundedRectangle(cornerRadius: 12))
                }

                Spacer(minLength: 20)
            }
            .padding()
        }
        .navigationBarTitleDisplayMode(.inline)
        .toolbar {
            ToolbarItem(placement: .navigationBarTrailing) {
                Button("分享") {
                    // TODO: 分享作业信息
                }
            }
        }
    }
}

#Preview {
    AssignmentListView()
        .environmentObject(AssignmentManager())
}
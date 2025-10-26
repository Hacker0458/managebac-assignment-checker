//
//  AssignmentListView.swift
//  ManageBacCheckerFeature
//
//  Created by AI Assistant on 2025/1/27.
//  作业列表视图 - 显示所有作业并支持筛选和排序
//

import SwiftUI
import Foundation

@MainActor
public struct AssignmentListView: View {
    @EnvironmentObject private var assignmentManager: AssignmentManager
    @State private var selectedFilter: AssignmentFilter = .all
    @State private var selectedSort: AssignmentSort = .dueDate
    @State private var searchText = ""
    @State private var showingAddAssignment = false
    @State private var showingFilters = false

    public init() {}

    public var body: some View {
        NavigationView {
            VStack(spacing: 0) {
                // 搜索栏
                searchBar

                // 筛选和排序栏
                filterBar

                // 作业列表
                assignmentList
            }
            .navigationTitle("作业列表")
            .toolbar {
                ToolbarItem(placement: .navigationBarLeading) {
                    Button(action: {
                        showingFilters = true
                    }) {
                        Image(systemName: "line.3.horizontal.decrease.circle")
                    }
                }

                ToolbarItem(placement: .navigationBarTrailing) {
                    Button(action: {
                        showingAddAssignment = true
                    }) {
                        Image(systemName: "plus")
                    }
                }
            }
        }
        .sheet(isPresented: $showingAddAssignment) {
            AddAssignmentView()
        }
        .sheet(isPresented: $showingFilters) {
            FilterView(
                selectedFilter: $selectedFilter,
                selectedSort: $selectedSort
            )
        }
        .task {
            // 使用.task修饰符进行异步操作
            if assignmentManager.assignments.isEmpty {
                await assignmentManager.refreshAssignments()
            }
        }
    }

    // MARK: - 搜索栏
    private var searchBar: some View {
        HStack {
            Image(systemName: "magnifyingglass")
                .foregroundColor(.secondary)

            TextField("搜索作业...", text: $searchText)
                .textFieldStyle(PlainTextFieldStyle())

            if !searchText.isEmpty {
                Button(action: {
                    searchText = ""
                }) {
                    Image(systemName: "xmark.circle.fill")
                        .foregroundColor(.secondary)
                }
            }
        }
        .padding(.horizontal, 12)
        .padding(.vertical, 8)
        .background(Color(.systemGray6))
        .clipShape(RoundedRectangle(cornerRadius: 10))
        .padding(.horizontal)
        .padding(.top, 8)
    }

    // MARK: - 筛选栏
    private var filterBar: some View {
        ScrollView(.horizontal, showsIndicators: false) {
            HStack(spacing: 12) {
                FilterChip(
                    title: "全部",
                    isSelected: selectedFilter == .all
                ) {
                    selectedFilter = .all
                }

                FilterChip(
                    title: "待完成",
                    isSelected: selectedFilter == .pending
                ) {
                    selectedFilter = .pending
                }

                FilterChip(
                    title: "已完成",
                    isSelected: selectedFilter == .completed
                ) {
                    selectedFilter = .completed
                }

                FilterChip(
                    title: "已逾期",
                    isSelected: selectedFilter == .overdue
                ) {
                    selectedFilter = .overdue
                }

                FilterChip(
                    title: "高优先级",
                    isSelected: selectedFilter == .highPriority
                ) {
                    selectedFilter = .highPriority
                }
            }
            .padding(.horizontal)
        }
        .padding(.vertical, 8)
    }

    // MARK: - 作业列表
    private var assignmentList: some View {
        Group {
            if filteredAssignments.isEmpty {
                emptyState
            } else {
                List {
                    ForEach(groupedAssignments.keys.sorted(by: { $0 < $1 }), id: \.self) { section in
                        Section(header: Text(section)) {
                            ForEach(groupedAssignments[section] ?? []) { assignment in
                                AssignmentDetailRowView(assignment: assignment)
                                    .swipeActions(edge: .trailing, allowsFullSwipe: false) {
                                        Button("完成") {
                                            toggleAssignmentCompletion(assignment)
                                        }
                                        .tint(.green)

                                        Button("删除") {
                                            deleteAssignment(assignment)
                                        }
                                        .tint(.red)
                                    }
                            }
                        }
                    }
                }
                .listStyle(PlainListStyle())
            }
        }
    }

    // MARK: - 空状态
    private var emptyState: some View {
        VStack(spacing: 16) {
            Image(systemName: "doc.text")
                .font(.system(size: 60))
                .foregroundColor(.secondary)

            Text("没有找到作业")
                .font(.headline)
                .foregroundColor(.primary)

            Text("尝试调整筛选条件或添加新作业")
                .font(.subheadline)
                .foregroundColor(.secondary)
                .multilineTextAlignment(.center)

            Button(action: {
                showingAddAssignment = true
            }) {
                HStack {
                    Image(systemName: "plus")
                    Text("添加作业")
                }
                .foregroundColor(.white)
                .padding()
                .background(Color.blue)
                .clipShape(RoundedRectangle(cornerRadius: 8))
            }
        }
        .frame(maxWidth: .infinity, maxHeight: .infinity)
        .padding()
    }

    // MARK: - 计算属性
    private var filteredAssignments: [Assignment] {
        let assignments = assignmentManager.assignments

        let filtered = assignments.filter { assignment in
            // 搜索过滤 - 优化性能
            let matchesSearch = searchText.isEmpty || {
                let searchLowercased = searchText.lowercased()
                return assignment.title.lowercased().contains(searchLowercased) ||
                       assignment.subject.lowercased().contains(searchLowercased)
            }()

            // 状态过滤
            let matchesFilter: Bool
            switch selectedFilter {
            case .all:
                matchesFilter = true
            case .pending:
                matchesFilter = assignment.status == .notSubmitted
            case .completed:
                matchesFilter = assignment.status == .submitted || assignment.status == .graded
            case .overdue:
                matchesFilter = assignment.status == .late
            case .highPriority:
                matchesFilter = assignment.priority == .high
            }

            return matchesSearch && matchesFilter
        }

        // 排序 - 优化性能
        return filtered.sorted { (assignment1: Assignment, assignment2: Assignment) in
            switch selectedSort {
            case .dueDate:
                return (assignment1.dueDate ?? Date.distantFuture) < (assignment2.dueDate ?? Date.distantFuture)
            case .title:
                return assignment1.title.localizedCompare(assignment2.title) == .orderedAscending
            case .subject:
                return assignment1.subject.localizedCompare(assignment2.subject) == .orderedAscending
            case .priority:
                let priorityOrder: [Assignment.Priority] = [.high, .medium, .low]
                let index1 = priorityOrder.firstIndex(of: assignment1.priority) ?? 0
                let index2 = priorityOrder.firstIndex(of: assignment2.priority) ?? 0
                return index1 < index2
            case .status:
                let statusOrder: [Assignment.AssignmentStatus] = [.notSubmitted, .late, .submitted, .graded]
                let index1 = statusOrder.firstIndex(of: assignment1.status) ?? 0
                let index2 = statusOrder.firstIndex(of: assignment2.status) ?? 0
                return index1 < index2
            }
        }
    }

    private var groupedAssignments: [String: [Assignment]] {
        Dictionary(grouping: filteredAssignments) { assignment in
            if let dueDate = assignment.dueDate {
                let formatter = DateFormatter()
                formatter.dateFormat = "yyyy年MM月dd日"
                return formatter.string(from: dueDate)
            } else {
                return "无截止日期"
            }
        }
    }

    // MARK: - 操作方法
    private func toggleAssignmentCompletion(_ assignment: Assignment) {
        // 这里应该调用AssignmentManager的方法来更新作业状态
        // assignmentManager.toggleAssignmentCompletion(assignment)
    }

    private func deleteAssignment(_ assignment: Assignment) {
        // 这里应该调用AssignmentManager的方法来删除作业
        // assignmentManager.deleteAssignment(assignment)
    }
}

// MARK: - 筛选芯片
@MainActor
public struct FilterChip: View {
    let title: String
    let isSelected: Bool
    let action: () -> Void

    public init(title: String, isSelected: Bool, action: @escaping () -> Void) {
        self.title = title
        self.isSelected = isSelected
        self.action = action
    }

    public var body: some View {
        Button(action: action) {
            Text(title)
                .font(.subheadline)
                .fontWeight(.medium)
                .foregroundColor(isSelected ? .white : .primary)
                .padding(.horizontal, 16)
                .padding(.vertical, 8)
                .background(isSelected ? Color.blue : Color(.systemGray6))
                .clipShape(Capsule())
        }
        .buttonStyle(PlainButtonStyle())
    }
}

// MARK: - 作业详情行视图
@MainActor
public struct AssignmentDetailRowView: View {
    let assignment: Assignment

    public init(assignment: Assignment) {
        self.assignment = assignment
    }

    public var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            HStack {
                // 状态指示器
                Circle()
                    .fill(assignment.status.color)
                    .frame(width: 12, height: 12)

                VStack(alignment: .leading, spacing: 2) {
                    Text(assignment.title)
                        .font(.headline)
                        .fontWeight(.semibold)
                        .lineLimit(2)

                    Text(assignment.subject)
                        .font(.subheadline)
                        .foregroundColor(.secondary)
                }

                Spacer()

                VStack(alignment: .trailing, spacing: 4) {
                    // 优先级标签
                    PriorityTag(priority: assignment.priority)

                    // 截止日期
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
            }

            // 描述
            if !assignment.description.isEmpty {
                Text(assignment.description)
                    .font(.caption)
                    .foregroundColor(.secondary)
                    .lineLimit(2)
            }
        }
        .padding(.vertical, 4)
    }
}

// MARK: - 优先级标签
@MainActor
public struct PriorityTag: View {
    let priority: Assignment.Priority

    public init(priority: Assignment.Priority) {
        self.priority = priority
    }

    public var body: some View {
        Text(priority.localizedTitle)
            .font(.caption2)
            .fontWeight(.medium)
            .foregroundColor(.white)
            .padding(.horizontal, 6)
            .padding(.vertical, 2)
            .background(priority.color)
            .clipShape(Capsule())
    }
}

// MARK: - 筛选视图
@MainActor
public struct FilterView: View {
    @Binding var selectedFilter: AssignmentFilter
    @Binding var selectedSort: AssignmentSort
    @Environment(\.dismiss) private var dismiss

    public init(selectedFilter: Binding<AssignmentFilter>, selectedSort: Binding<AssignmentSort>) {
        self._selectedFilter = selectedFilter
        self._selectedSort = selectedSort
    }

    public var body: some View {
        NavigationView {
            Form {
                Section("筛选条件") {
                    Picker("状态", selection: $selectedFilter) {
                        ForEach(AssignmentFilter.allCases, id: \.self) { filter in
                            Text(filter.displayName).tag(filter)
                        }
                    }
                }

                Section("排序方式") {
                    Picker("排序", selection: $selectedSort) {
                        ForEach(AssignmentSort.allCases, id: \.self) { sort in
                            Text(sort.displayName).tag(sort)
                        }
                    }
                }
            }
            .navigationTitle("筛选和排序")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button("完成") {
                        dismiss()
                    }
                }
            }
        }
    }
}

// MARK: - 添加作业视图（简化版本）

// MARK: - 设置视图（简化版本）
@MainActor
public struct SettingsView: View {
    @Environment(\.dismiss) private var dismiss
    @EnvironmentObject private var assignmentManager: AssignmentManager

    public init() {}

    public var body: some View {
        NavigationView {
            Form {
                Section("账户设置") {
                    HStack {
                        Image(systemName: "person.circle.fill")
                            .foregroundColor(.blue)
                        Text("ManageBac账户")
                        Spacer()
                        Text("已连接")
                            .foregroundColor(.green)
                    }
                }

                Section("通知设置") {
                    Toggle("启用通知", isOn: .constant(true))
                    Toggle("截止日期提醒", isOn: .constant(true))
                }

                Section("数据同步") {
                    Button("立即同步") {
                        Task {
                            await assignmentManager.refreshAssignments()
                        }
                    }
                }
            }
            .navigationTitle("设置")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button("完成") {
                        dismiss()
                    }
                }
            }
        }
    }
}

// MARK: - 筛选和排序枚举
public enum AssignmentFilter: CaseIterable {
    case all, pending, completed, overdue, highPriority

    public var displayName: String {
        switch self {
        case .all: return "全部"
        case .pending: return "待完成"
        case .completed: return "已完成"
        case .overdue: return "已逾期"
        case .highPriority: return "高优先级"
        }
    }
}

public enum AssignmentSort: CaseIterable {
    case dueDate, title, subject, priority, status

    public var displayName: String {
        switch self {
        case .dueDate: return "截止日期"
        case .title: return "标题"
        case .subject: return "学科"
        case .priority: return "优先级"
        case .status: return "状态"
        }
    }
}

#Preview {
    AssignmentListView()
        .environmentObject(AssignmentManager())
}

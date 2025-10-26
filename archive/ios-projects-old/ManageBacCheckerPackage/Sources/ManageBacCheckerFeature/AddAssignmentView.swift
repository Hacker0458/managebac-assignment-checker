//
//  AddAssignmentView.swift
//  ManageBacCheckerFeature
//
//  Created by AI Assistant on 2025/1/27.
//  添加作业视图 - 允许用户手动添加作业
//

import SwiftUI

@MainActor
public struct AddAssignmentView: View {
    @EnvironmentObject private var assignmentManager: AssignmentManager
    @Environment(\.dismiss) private var dismiss
    
    @State private var title = ""
    @State private var subject = ""
    @State private var description = ""
    @State private var dueDate = Date()
    @State private var priority: Assignment.Priority = .medium
    @State private var status: Assignment.AssignmentStatus = .notSubmitted
    
    public init() {}
    
    public var body: some View {
        NavigationView {
            Form {
                Section("基本信息") {
                    TextField("作业标题", text: $title)
                    TextField("学科", text: $subject)
                    
                    TextField("描述", text: $description)
                        .lineLimit(3)
                }
                
                Section("详细信息") {
                    DatePicker("截止日期", selection: $dueDate, displayedComponents: [.date, .hourAndMinute])
                    
                    Picker("优先级", selection: $priority) {
                        ForEach(Assignment.Priority.allCases, id: \.self) { priority in
                            Text(priority.localizedTitle).tag(priority)
                        }
                    }
                    
                    Picker("状态", selection: $status) {
                        ForEach(Assignment.AssignmentStatus.allCases, id: \.self) { status in
                            Text(status.localizedTitle).tag(status)
                        }
                    }
                }
            }
            .navigationTitle("添加作业")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarLeading) {
                    Button("取消") {
                        dismiss()
                    }
                }
                
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button("保存") {
                        saveAssignment()
                    }
                    .disabled(title.isEmpty || subject.isEmpty)
                }
            }
        }
    }
    
    private func saveAssignment() {
        let newAssignment = Assignment(
            title: title,
            subject: subject,
            dueDate: dueDate,
            status: status,
            description: description,
            priority: priority
        )
        
        assignmentManager.assignments.append(newAssignment)
        // 保存作业后刷新数据
        Task {
            await assignmentManager.quickRefresh()
        }
        dismiss()
    }
}

#Preview {
    AddAssignmentView()
        .environmentObject(AssignmentManager())
}

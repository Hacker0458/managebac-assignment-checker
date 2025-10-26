//
//  ModernComponents.swift
//  ManageBacChecker
//
//  Created by Assistant on 2025/9/29.
//

import SwiftUI

// MARK: - 现代化统计卡片
struct ModernStatCard: View {
    let title: String
    let value: String
    let icon: String
    let color: Color
    let trend: TrendDirection?
    
    enum TrendDirection {
        case up, down, stable
        
        var icon: String {
            switch self {
            case .up: return "arrow.up.right"
            case .down: return "arrow.down.right"
            case .stable: return "minus"
            }
        }
        
        var color: Color {
            switch self {
            case .up: return .green
            case .down: return .red
            case .stable: return .gray
            }
        }
    }
    
    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            HStack {
                Image(systemName: icon)
                    .font(.title2)
                    .foregroundColor(color)
                    .frame(width: 32, height: 32)
                    .background(color.opacity(0.1))
                    .clipShape(RoundedRectangle(cornerRadius: 8))
                
                Spacer()
                
                if let trend = trend {
                    Image(systemName: trend.icon)
                        .font(.caption)
                        .foregroundColor(trend.color)
                        .padding(4)
                        .background(trend.color.opacity(0.1))
                        .clipShape(Circle())
                }
            }
            
            VStack(alignment: .leading, spacing: 4) {
                Text(value)
                    .font(.title)
                    .fontWeight(.bold)
                    .foregroundColor(.primary)
                
                Text(title)
                    .font(.caption)
                    .foregroundColor(.secondary)
            }
        }
        .padding(16)
        .background(
            RoundedRectangle(cornerRadius: 16)
                .fill(.ultraThinMaterial)
                .shadow(color: .black.opacity(0.05), radius: 8, x: 0, y: 4)
        )
    }
}

// MARK: - 现代化作业卡片
struct ModernAssignmentCard: View {
    let assignment: Assignment
    @Environment(\.colorScheme) var colorScheme
    
    var body: some View {
        HStack(spacing: 16) {
            // 状态指示器
            VStack {
                Circle()
                    .fill(assignment.status.color)
                    .frame(width: 12, height: 12)
                
                Rectangle()
                    .fill(assignment.status.color.opacity(0.3))
                    .frame(width: 2)
            }
            
            VStack(alignment: .leading, spacing: 8) {
                // 标题和科目
                HStack {
                    VStack(alignment: .leading, spacing: 4) {
                        Text(assignment.title)
                            .font(.headline)
                            .fontWeight(.semibold)
                            .lineLimit(2)
                        
                        Text(assignment.subject)
                            .font(.caption)
                            .padding(.horizontal, 8)
                            .padding(.vertical, 4)
                            .background(Color.blue.opacity(0.1))
                            .foregroundColor(.blue)
                            .clipShape(Capsule())
                    }
                    
                    Spacer()
                    
                    // 优先级指示器
                    if assignment.priority == .high {
                        Image(systemName: "exclamationmark.triangle.fill")
                            .foregroundColor(.red)
                            .font(.caption)
                    }
                }
                
                // 截止日期
                if let dueDate = assignment.dueDate {
                    HStack(spacing: 4) {
                        Image(systemName: "clock")
                            .font(.caption)
                            .foregroundColor(.secondary)
                        
                        Text(formatDueDate(dueDate))
                            .font(.caption)
                            .foregroundColor(.secondary)
                        
                        Spacer()
                        
                        // 剩余时间
                        Text(timeRemaining(until: dueDate))
                            .font(.caption)
                            .fontWeight(.medium)
                            .foregroundColor(timeRemainingColor(until: dueDate))
                    }
                }
            }
        }
        .padding(16)
        .background(
            RoundedRectangle(cornerRadius: 12)
                .fill(colorScheme == .dark ? Color(.systemGray6) : .white)
                .shadow(color: .black.opacity(0.05), radius: 4, x: 0, y: 2)
        )
    }
    
    private func formatDueDate(_ date: Date) -> String {
        let formatter = DateFormatter()
        formatter.dateStyle = .medium
        formatter.timeStyle = .short
        formatter.locale = Locale(identifier: "zh_CN")
        return formatter.string(from: date)
    }
    
    private func timeRemaining(until date: Date) -> String {
        let now = Date()
        let timeInterval = date.timeIntervalSince(now)
        
        if timeInterval < 0 {
            return "已过期"
        } else if timeInterval < 3600 {
            return "1小时内"
        } else if timeInterval < 86400 {
            let hours = Int(timeInterval / 3600)
            return "\(hours)小时后"
        } else {
            let days = Int(timeInterval / 86400)
            return "\(days)天后"
        }
    }
    
    private func timeRemainingColor(until date: Date) -> Color {
        let timeInterval = date.timeIntervalSince(Date())
        
        if timeInterval < 0 {
            return .red
        } else if timeInterval < 86400 {
            return .orange
        } else {
            return .green
        }
    }
}

// MARK: - 空状态视图
struct ModernEmptyStateView: View {
    let title: String
    let subtitle: String
    let icon: String
    let actionTitle: String?
    let action: (() -> Void)?
    
    var body: some View {
        VStack(spacing: 24) {
            Image(systemName: icon)
                .font(.system(size: 64, weight: .thin))
                .foregroundStyle(
                    LinearGradient(
                        colors: [.blue.opacity(0.6), .purple.opacity(0.6)],
                        startPoint: .topLeading,
                        endPoint: .bottomTrailing
                    )
                )
            
            VStack(spacing: 8) {
                Text(title)
                    .font(.title2)
                    .fontWeight(.semibold)
                    .multilineTextAlignment(.center)
                
                Text(subtitle)
                    .font(.body)
                    .foregroundColor(.secondary)
                    .multilineTextAlignment(.center)
            }
            
            if let actionTitle = actionTitle, let action = action {
                Button(action: action) {
                    Text(actionTitle)
                        .font(.headline)
                        .fontWeight(.semibold)
                        .foregroundColor(.white)
                        .padding(.horizontal, 24)
                        .padding(.vertical, 12)
                        .background(
                            LinearGradient(
                                colors: [.blue, .purple],
                                startPoint: .leading,
                                endPoint: .trailing
                            )
                        )
                        .clipShape(Capsule())
                }
            }
        }
        .padding(40)
    }
}

// MARK: - 加载视图
struct ModernLoadingView: View {
    @State private var isAnimating = false
    
    var body: some View {
        VStack(spacing: 16) {
            ZStack {
                Circle()
                    .stroke(Color.blue.opacity(0.2), lineWidth: 4)
                    .frame(width: 50, height: 50)
                
                Circle()
                    .trim(from: 0, to: 0.7)
                    .stroke(
                        LinearGradient(
                            colors: [.blue, .purple],
                            startPoint: .leading,
                            endPoint: .trailing
                        ),
                        style: StrokeStyle(lineWidth: 4, lineCap: .round)
                    )
                    .frame(width: 50, height: 50)
                    .rotationEffect(.degrees(isAnimating ? 360 : 0))
                    .animation(
                        .linear(duration: 1).repeatForever(autoreverses: false),
                        value: isAnimating
                    )
            }
            
            Text("正在同步数据...")
                .font(.subheadline)
                .foregroundColor(.secondary)
        }
        .onAppear {
            isAnimating = true
        }
    }
}

// MARK: - 成功反馈视图
struct SuccessFeedbackView: View {
    let message: String
    @State private var scale = 0.5
    @State private var opacity = 0.0
    
    var body: some View {
        VStack(spacing: 12) {
            Image(systemName: "checkmark.circle.fill")
                .font(.system(size: 50))
                .foregroundColor(.green)
                .scaleEffect(scale)
                .opacity(opacity)
            
            Text(message)
                .font(.headline)
                .fontWeight(.semibold)
                .opacity(opacity)
        }
        .onAppear {
            withAnimation(.spring(response: 0.6, dampingFraction: 0.8)) {
                scale = 1.0
                opacity = 1.0
            }
        }
    }
}

// MARK: - 预览
#Preview("ModernStatCard") {
    ModernStatCard(
        title: "待完成",
        value: "5",
        icon: "clock.fill",
        color: .orange,
        trend: .up
    )
    .padding()
}

#Preview("ModernAssignmentCard") {
    ModernAssignmentCard(
        assignment: Assignment(
            title: "数学作业 - 微积分练习",
            subject: "数学",
            dueDate: Date().addingTimeInterval(86400),
            status: .notSubmitted,
            description: "完成第5章练习题",
            priority: .high
        )
    )
    .padding()
}

#Preview("ModernEmptyStateView") {
    ModernEmptyStateView(
        title: "暂无作业",
        subtitle: "连接到 ManageBac 后将显示您的作业",
        icon: "doc.text",
        actionTitle: "立即连接",
        action: { }
    )
}

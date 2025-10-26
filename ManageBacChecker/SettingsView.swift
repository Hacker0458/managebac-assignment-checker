//
//  SettingsView.swift
//  ManageBac Assignment Checker
//
//  Created by 方籽杰 on 2025/9/26.
//  设置视图 - 配置ManageBac账户和应用设置
//

import SwiftUI

struct SettingsView: View {
    @EnvironmentObject var assignmentManager: AssignmentManager
    @StateObject private var notificationManager = NotificationManager.shared
    
    @State private var showingLoginSheet = false
    @State private var showingAbout = false
    @State private var pendingNotificationsCount = 0
    @State private var showingCredentialsSheet = false
    @State private var showingAboutSheet = false
    @State private var showingNotificationSettings = false

    var body: some View {
        NavigationView {
            List {
                // 账户设置
                Section("账户设置") {
                    Button {
                        showingCredentialsSheet = true
                    } label: {
                        HStack {
                            Image(systemName: "person.circle")
                                .foregroundColor(.blue)
                                .font(.system(size: 20))

                            VStack(alignment: .leading, spacing: 2) {
                                Text("ManageBac 账户")
                                    .foregroundColor(.primary)

                                if assignmentManager.config.email.isEmpty {
                                    Text("未配置")
                                        .font(.caption)
                                        .foregroundColor(.orange)
                                } else {
                                    Text(assignmentManager.config.email)
                                        .font(.caption)
                                        .foregroundColor(.secondary)
                                }
                            }

                            Spacer()

                            if assignmentManager.isLoggedIn {
                                Image(systemName: "checkmark.circle.fill")
                                    .foregroundColor(.green)
                            } else if !assignmentManager.config.email.isEmpty {
                                Image(systemName: "exclamationmark.triangle.fill")
                                    .foregroundColor(.orange)
                            }
                        }
                    }

                    HStack {
                        Image(systemName: "arrow.clockwise")
                            .foregroundColor(.blue)
                            .font(.system(size: 20))

                        Text("自动刷新间隔")

                        Spacer()

                        Picker("", selection: $assignmentManager.config.autoRefreshInterval) {
                            Text("15分钟").tag(TimeInterval(15 * 60))
                            Text("30分钟").tag(TimeInterval(30 * 60))
                            Text("1小时").tag(TimeInterval(60 * 60))
                            Text("2小时").tag(TimeInterval(2 * 60 * 60))
                        }
                        .pickerStyle(MenuPickerStyle())
                        .onChange(of: assignmentManager.config.autoRefreshInterval) { _ in
                            assignmentManager.saveConfiguration()
                        }
                    }
                }

                // 通知设置
                Section("通知设置") {
                    Toggle(isOn: $assignmentManager.config.enableNotifications) {
                        HStack {
                            Image(systemName: "bell")
                                .foregroundColor(.blue)
                                .font(.system(size: 20))

                            VStack(alignment: .leading, spacing: 2) {
                                Text("推送通知")
                                Text("作业截止提醒")
                                    .font(.caption)
                                    .foregroundColor(.secondary)
                            }
                        }
                    }
                    .onChange(of: assignmentManager.config.enableNotifications) { _ in
                        assignmentManager.saveConfiguration()
                    }

                    Button {
                        showingNotificationSettings = true
                    } label: {
                        HStack {
                            Image(systemName: "gear")
                                .foregroundColor(.blue)
                                .font(.system(size: 20))

                            Text("通知设置")
                                .foregroundColor(.primary)

                            Spacer()

                            Image(systemName: "chevron.right")
                                .font(.caption)
                                .foregroundColor(.secondary)
                        }
                    }
                }

                // 数据管理
                Section("数据管理") {
                    Button {
                        Task {
                            await assignmentManager.fetchAssignments()
                        }
                    } label: {
                        HStack {
                            Image(systemName: "arrow.clockwise")
                                .foregroundColor(.blue)
                                .font(.system(size: 20))

                            VStack(alignment: .leading, spacing: 2) {
                                Text("立即同步")
                                    .foregroundColor(.primary)

                                if let lastUpdate = assignmentManager.lastUpdateTime {
                                    Text("上次更新: \(lastUpdate.formatted(.dateTime.month().day().hour().minute()))")
                                        .font(.caption)
                                        .foregroundColor(.secondary)
                                } else {
                                    Text("尚未同步")
                                        .font(.caption)
                                        .foregroundColor(.orange)
                                }
                            }

                            Spacer()

                            if assignmentManager.isLoading {
                                ProgressView()
                                    .scaleEffect(0.8)
                            }
                        }
                    }
                    .disabled(assignmentManager.isLoading)

                    Button {
                        clearCachedData()
                    } label: {
                        HStack {
                            Image(systemName: "trash")
                                .foregroundColor(.red)
                                .font(.system(size: 20))

                            Text("清除缓存数据")
                                .foregroundColor(.red)
                        }
                    }
                }

                // 应用信息
                Section("应用信息") {
                    Button {
                        showingAboutSheet = true
                    } label: {
                        HStack {
                            Image(systemName: "info.circle")
                                .foregroundColor(.blue)
                                .font(.system(size: 20))

                            Text("关于应用")
                                .foregroundColor(.primary)

                            Spacer()

                            Text("v1.0.0")
                                .font(.caption)
                                .foregroundColor(.secondary)

                            Image(systemName: "chevron.right")
                                .font(.caption)
                                .foregroundColor(.secondary)
                        }
                    }

                    Button {
                        if let url = URL(string: "https://github.com/Hacker0458/managebac-assignment-checker") {
                            UIApplication.shared.open(url)
                        }
                    } label: {
                        HStack {
                            Image(systemName: "link")
                                .foregroundColor(.blue)
                                .font(.system(size: 20))

                            Text("GitHub 项目")
                                .foregroundColor(.primary)

                            Spacer()

                            Image(systemName: "arrow.up.right")
                                .font(.caption)
                                .foregroundColor(.secondary)
                        }
                    }

                    Button {
                        provideFeedback()
                    } label: {
                        HStack {
                            Image(systemName: "envelope")
                                .foregroundColor(.blue)
                                .font(.system(size: 20))

                            Text("反馈建议")
                                .foregroundColor(.primary)

                            Spacer()

                            Image(systemName: "arrow.up.right")
                                .font(.caption)
                                .foregroundColor(.secondary)
                        }
                    }
                }
            }
            .navigationTitle("设置")
        }
        .sheet(isPresented: $showingCredentialsSheet) {
            CredentialsConfigView()
        }
        .sheet(isPresented: $showingAboutSheet) {
            AboutView()
        }
        .sheet(isPresented: $showingNotificationSettings) {
            NotificationSettingsView()
        }
    }

    private func clearCachedData() {
        UserDefaults.standard.removeObject(forKey: "CachedAssignments")
        assignmentManager.assignments.removeAll()
        assignmentManager.lastUpdateTime = nil

        // 显示确认消息
        let impactFeedback = UIImpactFeedbackGenerator(style: .medium)
        impactFeedback.impactOccurred()
    }

    private func provideFeedback() {
        let subject = "ManageBac Assignment Checker - 反馈"
        let body = """
        感谢您使用 ManageBac Assignment Checker！

        请在此处写下您的反馈、建议或遇到的问题：


        ---
        应用版本: 1.0.0
        iOS 版本: \(UIDevice.current.systemVersion)
        设备型号: \(UIDevice.current.model)
        """

        if let url = URL(string: "mailto:?subject=\(subject.addingPercentEncoding(withAllowedCharacters: .urlQueryAllowed) ?? "")&body=\(body.addingPercentEncoding(withAllowedCharacters: .urlQueryAllowed) ?? "")") {
            UIApplication.shared.open(url)
        }
    }
}

// MARK: - 凭据配置视图
struct CredentialsConfigView: View {
    @EnvironmentObject var assignmentManager: AssignmentManager
    @Environment(\.dismiss) private var dismiss

    @State private var email: String = ""
    @State private var password: String = ""
    @State private var schoolURL: String = ""
    @State private var isTestingLogin = false
    @State private var showingPassword = false

    var body: some View {
        NavigationView {
            Form {
                Section(header: Text("ManageBac 账户信息")) {
                    TextField("邮箱地址", text: $email)
                        .textContentType(.emailAddress)
                        .keyboardType(.emailAddress)
                        .autocapitalization(.none)

                    HStack {
                        if showingPassword {
                            TextField("密码", text: $password)
                                .textContentType(.password)
                        } else {
                            SecureField("密码", text: $password)
                                .textContentType(.password)
                        }

                        Button {
                            showingPassword.toggle()
                        } label: {
                            Image(systemName: showingPassword ? "eye.slash" : "eye")
                                .foregroundColor(.secondary)
                        }
                    }

                    TextField("学校网址", text: $schoolURL)
                        .textContentType(.URL)
                        .keyboardType(.URL)
                        .autocapitalization(.none)
                        .placeholder(when: schoolURL.isEmpty) {
                            Text("https://your-school.managebac.cn")
                                .foregroundColor(.secondary)
                        }
                }

                Section(footer: Text("这些信息将安全地存储在您的设备上，仅用于连接到 ManageBac 服务器。")) {
                    Button {
                        testLogin()
                    } label: {
                        HStack {
                            if isTestingLogin {
                                ProgressView()
                                    .scaleEffect(0.8)
                            } else {
                                Image(systemName: "checkmark.shield")
                            }

                            Text("测试连接")
                        }
                    }
                    .disabled(email.isEmpty || password.isEmpty || schoolURL.isEmpty || isTestingLogin)
                }
            }
            .navigationTitle("账户配置")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarLeading) {
                    Button("取消") {
                        dismiss()
                    }
                }

                ToolbarItem(placement: .navigationBarTrailing) {
                    Button("保存") {
                        saveCredentials()
                        dismiss()
                    }
                    .disabled(email.isEmpty || password.isEmpty || schoolURL.isEmpty)
                }
            }
        }
        .onAppear {
            loadCurrentCredentials()
        }
    }

    private func loadCurrentCredentials() {
        email = assignmentManager.config.email
        password = assignmentManager.config.password
        schoolURL = assignmentManager.config.schoolURL
    }

    private func saveCredentials() {
        assignmentManager.config.email = email
        assignmentManager.config.password = password
        assignmentManager.config.schoolURL = schoolURL.trimmingCharacters(in: .whitespacesAndNewlines)

        assignmentManager.saveConfiguration()

        // 保存后自动测试连接
        Task {
            await assignmentManager.fetchAssignments()
        }
    }

    private func testLogin() {
        isTestingLogin = true

        // 临时保存凭据进行测试
        let tempConfig = assignmentManager.config
        assignmentManager.config.email = email
        assignmentManager.config.password = password
        assignmentManager.config.schoolURL = schoolURL.trimmingCharacters(in: .whitespacesAndNewlines)

        Task {
            await assignmentManager.fetchAssignments()

            await MainActor.run {
                isTestingLogin = false

                // 如果测试失败，恢复原配置
                if !assignmentManager.isLoggedIn {
                    assignmentManager.config = tempConfig
                }
            }
        }
    }
}

// MARK: - 通知设置视图
struct NotificationSettingsView: View {
    @Environment(\.dismiss) private var dismiss

    var body: some View {
        NavigationView {
            List {
                Section(header: Text("通知类型")) {
                    HStack {
                        Image(systemName: "bell.badge")
                            .foregroundColor(.blue)
                        VStack(alignment: .leading) {
                            Text("作业截止提醒")
                            Text("在作业截止前一天提醒")
                                .font(.caption)
                                .foregroundColor(.secondary)
                        }
                        Spacer()
                        Toggle("", isOn: .constant(true))
                    }

                    HStack {
                        Image(systemName: "clock.badge.exclamationmark")
                            .foregroundColor(.orange)
                        VStack(alignment: .leading) {
                            Text("逾期提醒")
                            Text("作业逾期时立即通知")
                                .font(.caption)
                                .foregroundColor(.secondary)
                        }
                        Spacer()
                        Toggle("", isOn: .constant(true))
                    }
                }

                Section(header: Text("系统设置")) {
                    Button("打开系统通知设置") {
                        if let url = URL(string: UIApplication.openSettingsURLString) {
                            UIApplication.shared.open(url)
                        }
                    }
                }
            }
            .navigationTitle("通知设置")
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

// MARK: - 关于视图
struct AboutView: View {
    @Environment(\.dismiss) private var dismiss

    var body: some View {
        NavigationView {
            ScrollView {
                VStack(spacing: 20) {
                    // 应用图标和名称
                    VStack(spacing: 12) {
                        Image(systemName: "graduationcap.circle.fill")
                            .font(.system(size: 80))
                            .foregroundColor(.blue)

                        Text("ManageBac Assignment Checker")
                            .font(.title2)
                            .fontWeight(.bold)
                            .multilineTextAlignment(.center)

                        Text("版本 1.0.0")
                            .font(.subheadline)
                            .foregroundColor(.secondary)
                    }

                    // 应用描述
                    VStack(alignment: .leading, spacing: 12) {
                        Text("关于应用")
                            .font(.headline)

                        Text("ManageBac Assignment Checker 是一个智能的作业管理工具，帮助学生轻松跟踪和管理 ManageBac 平台上的作业。")
                            .font(.body)
                            .foregroundColor(.secondary)

                        Text("主要功能：")
                            .font(.subheadline)
                            .fontWeight(.semibold)

                        VStack(alignment: .leading, spacing: 4) {
                            FeatureRow(icon: "list.bullet.clipboard", text: "自动同步作业信息")
                            FeatureRow(icon: "bell.badge", text: "智能截止日期提醒")
                            FeatureRow(icon: "chart.bar.fill", text: "详细的统计分析")
                            FeatureRow(icon: "iphone", text: "现代化 iOS 界面")
                        }
                    }
                    .padding()
                    .background(Color(UIColor.secondarySystemBackground))
                    .clipShape(RoundedRectangle(cornerRadius: 12))

                    // 致谢
                    VStack(alignment: .leading, spacing: 12) {
                        Text("致谢")
                            .font(.headline)

                        Text("本应用基于开源的 Python 版本 ManageBac Assignment Checker 项目开发，感谢原项目的贡献者们。")
                            .font(.body)
                            .foregroundColor(.secondary)

                        Text("特别感谢所有提供反馈和建议的用户。")
                            .font(.body)
                            .foregroundColor(.secondary)
                    }
                    .padding()
                    .background(Color(UIColor.secondarySystemBackground))
                    .clipShape(RoundedRectangle(cornerRadius: 12))

                    Spacer(minLength: 20)
                }
                .padding()
            }
            .navigationTitle("关于")
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

// MARK: - 功能行组件
struct FeatureRow: View {
    let icon: String
    let text: String

    var body: some View {
        HStack(spacing: 8) {
            Image(systemName: icon)
                .font(.system(size: 14))
                .foregroundColor(.blue)
                .frame(width: 20)

            Text(text)
                .font(.subheadline)
        }
    }
}

// MARK: - 扩展
extension View {
    func placeholder<Content: View>(
        when shouldShow: Bool,
        alignment: Alignment = .leading,
        @ViewBuilder placeholder: () -> Content) -> some View {

        ZStack(alignment: alignment) {
            placeholder().opacity(shouldShow ? 1 : 0)
            self
        }
    }
}

#Preview {
    SettingsView()
        .environmentObject(AssignmentManager())
}


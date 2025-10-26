//
//  OnboardingView.swift
//  ManageBacChecker
//
//  Created by Assistant on 2025/9/29.
//

import SwiftUI

struct OnboardingView: View {
    @State private var currentPage = 0
    @State private var showingLoginSetup = false
    @Binding var isOnboardingComplete: Bool
    
    let pages = [
        OnboardingPage(
            title: "欢迎使用\nManageBac助手",
            subtitle: "智能管理您的学习任务",
            description: "自动同步作业信息，智能提醒截止日期，让学习更高效",
            imageName: "graduationcap.circle.fill",
            color: .blue
        ),
        OnboardingPage(
            title: "实时同步\n作业信息",
            subtitle: "与ManageBac无缝连接",
            description: "安全连接到您的学校ManageBac系统，实时获取最新的作业和任务信息",
            imageName: "arrow.triangle.2.circlepath.circle.fill",
            color: .green
        ),
        OnboardingPage(
            title: "智能提醒\n不错过任何截止日期",
            subtitle: "个性化通知系统",
            description: "根据作业优先级和截止时间，智能安排提醒，确保您按时完成每一项任务",
            imageName: "bell.badge.circle.fill",
            color: .orange
        ),
        OnboardingPage(
            title: "数据统计\n学习进度一目了然",
            subtitle: "可视化学习分析",
            description: "详细的统计图表帮您了解学习习惯，优化时间管理，提升学习效率",
            imageName: "chart.bar.fill",
            color: .purple
        )
    ]
    
    var body: some View {
        GeometryReader { geometry in
            VStack(spacing: 0) {
                // 页面指示器
                HStack(spacing: 8) {
                    ForEach(0..<pages.count, id: \.self) { index in
                        Capsule()
                            .fill(currentPage == index ? pages[currentPage].color : Color.gray.opacity(0.3))
                            .frame(width: currentPage == index ? 30 : 8, height: 8)
                            .animation(.easeInOut(duration: 0.3), value: currentPage)
                    }
                }
                .padding(.top, 50)
                
                // 主要内容
                TabView(selection: $currentPage) {
                    ForEach(0..<pages.count, id: \.self) { index in
                        OnboardingPageView(page: pages[index])
                            .tag(index)
                    }
                }
                .tabViewStyle(PageTabViewStyle(indexDisplayMode: .never))
                .animation(.easeInOut, value: currentPage)
                
                // 底部按钮
                VStack(spacing: 20) {
                    if currentPage < pages.count - 1 {
                        // 下一页按钮
                        Button(action: {
                            withAnimation {
                                currentPage += 1
                            }
                        }) {
                            HStack {
                                Text("继续")
                                    .font(.headline)
                                    .fontWeight(.semibold)
                                
                                Image(systemName: "arrow.right")
                                    .font(.headline)
                            }
                            .foregroundColor(.white)
                            .frame(maxWidth: .infinity)
                            .frame(height: 56)
                            .background(
                                LinearGradient(
                                    colors: [pages[currentPage].color, pages[currentPage].color.opacity(0.8)],
                                    startPoint: .leading,
                                    endPoint: .trailing
                                )
                            )
                            .cornerRadius(28)
                        }
                        
                        // 跳过按钮
                        Button("跳过") {
                            showingLoginSetup = true
                        }
                        .foregroundColor(.secondary)
                        .font(.subheadline)
                        
                    } else {
                        // 开始使用按钮
                        Button(action: {
                            showingLoginSetup = true
                        }) {
                            HStack {
                                Text("开始使用")
                                    .font(.headline)
                                    .fontWeight(.semibold)
                                
                                Image(systemName: "arrow.right.circle.fill")
                                    .font(.headline)
                            }
                            .foregroundColor(.white)
                            .frame(maxWidth: .infinity)
                            .frame(height: 56)
                            .background(
                                LinearGradient(
                                    colors: [.blue, .purple],
                                    startPoint: .leading,
                                    endPoint: .trailing
                                )
                            )
                            .cornerRadius(28)
                        }
                        .scaleEffect(1.05)
                        .animation(.easeInOut(duration: 0.3).repeatCount(3, autoreverses: true), value: currentPage)
                    }
                }
                .padding(.horizontal, 32)
                .padding(.bottom, geometry.safeAreaInsets.bottom + 20)
            }
        }
        .background(
            LinearGradient(
                colors: [
                    pages[currentPage].color.opacity(0.1),
                    pages[currentPage].color.opacity(0.05),
                    Color.clear
                ],
                startPoint: .top,
                endPoint: .bottom
            )
        )
        .sheet(isPresented: $showingLoginSetup) {
            LoginSetupView(isOnboardingComplete: $isOnboardingComplete)
        }
        .onAppear {
            // 请求通知权限
            NotificationManager.shared.setupNotificationActions()
        }
    }
}

struct OnboardingPageView: View {
    let page: OnboardingPage
    
    var body: some View {
        VStack(spacing: 40) {
            Spacer()
            
            // 图标
            Image(systemName: page.imageName)
                .font(.system(size: 120, weight: .thin))
                .foregroundStyle(
                    LinearGradient(
                        colors: [page.color, page.color.opacity(0.7)],
                        startPoint: .topLeading,
                        endPoint: .bottomTrailing
                    )
                )
                .shadow(color: page.color.opacity(0.3), radius: 20, x: 0, y: 10)
            
            VStack(spacing: 16) {
                // 标题
                Text(page.title)
                    .font(.largeTitle)
                    .fontWeight(.bold)
                    .multilineTextAlignment(.center)
                    .foregroundStyle(
                        LinearGradient(
                            colors: [.primary, .primary.opacity(0.8)],
                            startPoint: .leading,
                            endPoint: .trailing
                        )
                    )
                
                // 副标题
                Text(page.subtitle)
                    .font(.title2)
                    .fontWeight(.medium)
                    .foregroundColor(page.color)
                    .multilineTextAlignment(.center)
                
                // 描述
                Text(page.description)
                    .font(.body)
                    .foregroundColor(.secondary)
                    .multilineTextAlignment(.center)
                    .lineLimit(3)
                    .padding(.horizontal, 20)
            }
            
            Spacer()
        }
        .padding(.horizontal, 32)
    }
}

struct OnboardingPage {
    let title: String
    let subtitle: String
    let description: String
    let imageName: String
    let color: Color
}

struct LoginSetupView: View {
    @Binding var isOnboardingComplete: Bool
    @Environment(\.dismiss) private var dismiss
    @StateObject private var networkManager = NetworkManager.shared
    
    @State private var email = ""
    @State private var password = ""
    @State private var schoolURL = "https://shtcs.managebac.cn"
    @State private var isLoading = false
    @State private var showingError = false
    @State private var errorMessage = ""
    @State private var loginSuccess = false
    
    var body: some View {
        NavigationView {
            ScrollView {
                VStack(spacing: 30) {
                    // 头部
                    VStack(spacing: 16) {
                        Image(systemName: "person.crop.circle.fill.badge.checkmark")
                            .font(.system(size: 60))
                            .foregroundStyle(
                                LinearGradient(
                                    colors: [.blue, .purple],
                                    startPoint: .topLeading,
                                    endPoint: .bottomTrailing
                                )
                            )
                        
                        Text("连接您的ManageBac账户")
                            .font(.title2)
                            .fontWeight(.bold)
                        
                        Text("输入您的学校ManageBac登录信息")
                            .font(.subheadline)
                            .foregroundColor(.secondary)
                            .multilineTextAlignment(.center)
                    }
                    .padding(.top, 20)
                    
                    // 表单
                    VStack(spacing: 20) {
                        // 学校URL
                        VStack(alignment: .leading, spacing: 8) {
                            Text("学校网址")
                                .font(.subheadline)
                                .fontWeight(.medium)
                                .foregroundColor(.primary)
                            
                            TextField("https://your-school.managebac.cn", text: $schoolURL)
                                .textFieldStyle(ModernTextFieldStyle())
                                .keyboardType(.URL)
                                .autocapitalization(.none)
                                .disableAutocorrection(true)
                        }
                        
                        // 邮箱
                        VStack(alignment: .leading, spacing: 8) {
                            Text("邮箱地址")
                                .font(.subheadline)
                                .fontWeight(.medium)
                                .foregroundColor(.primary)
                            
                            TextField("your.email@example.com", text: $email)
                                .textFieldStyle(ModernTextFieldStyle())
                                .keyboardType(.emailAddress)
                                .autocapitalization(.none)
                                .disableAutocorrection(true)
                        }
                        
                        // 密码
                        VStack(alignment: .leading, spacing: 8) {
                            Text("密码")
                                .font(.subheadline)
                                .fontWeight(.medium)
                                .foregroundColor(.primary)
                            
                            SecureField("输入您的密码", text: $password)
                                .textFieldStyle(ModernTextFieldStyle())
                        }
                        
                        // 测试连接按钮
                        Button(action: testConnection) {
                            HStack {
                                if isLoading {
                                    ProgressView()
                                        .scaleEffect(0.8)
                                        .tint(.white)
                                } else {
                                    Image(systemName: "checkmark.shield.fill")
                                        .font(.headline)
                                }
                                
                                Text(isLoading ? "连接中..." : "测试连接")
                                    .font(.headline)
                                    .fontWeight(.semibold)
                            }
                            .foregroundColor(.white)
                            .frame(maxWidth: .infinity)
                            .frame(height: 56)
                            .background(
                                LinearGradient(
                                    colors: canTestConnection ? [.blue, .blue.opacity(0.8)] : [.gray, .gray.opacity(0.8)],
                                    startPoint: .leading,
                                    endPoint: .trailing
                                )
                            )
                            .cornerRadius(28)
                        }
                        .disabled(!canTestConnection || isLoading)
                        
                        if loginSuccess {
                            HStack {
                                Image(systemName: "checkmark.circle.fill")
                                    .foregroundColor(.green)
                                Text("连接成功！")
                                    .font(.subheadline)
                                    .fontWeight(.medium)
                                    .foregroundColor(.green)
                            }
                            .padding()
                            .background(Color.green.opacity(0.1))
                            .cornerRadius(12)
                        }
                    }
                    .padding(.horizontal, 20)
                    
                    // 隐私说明
                    VStack(spacing: 8) {
                        HStack {
                            Image(systemName: "lock.shield.fill")
                                .foregroundColor(.green)
                            Text("您的信息安全存储在设备本地")
                                .font(.caption)
                                .foregroundColor(.secondary)
                        }
                        
                        Text("我们不会存储或分享您的登录凭据")
                            .font(.caption)
                            .foregroundColor(.secondary)
                            .multilineTextAlignment(.center)
                    }
                    .padding()
                    .background(Color.green.opacity(0.05))
                    .cornerRadius(12)
                    .padding(.horizontal, 20)
                    
                    Spacer(minLength: 50)
                }
            }
            .navigationTitle("账户设置")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarLeading) {
                    Button("稍后设置") {
                        isOnboardingComplete = true
                        dismiss()
                    }
                    .foregroundColor(.secondary)
                }
                
                if loginSuccess {
                    ToolbarItem(placement: .navigationBarTrailing) {
                        Button("完成") {
                            completeSetup()
                        }
                        .fontWeight(.semibold)
                    }
                }
            }
        }
        .alert("连接失败", isPresented: $showingError) {
            Button("确定") { }
        } message: {
            Text(errorMessage)
        }
    }
    
    private var canTestConnection: Bool {
        !email.isEmpty && !password.isEmpty && !schoolURL.isEmpty
    }
    
    private func testConnection() {
        isLoading = true
        loginSuccess = false
        
        Task {
            let success = await networkManager.login(
                email: email,
                password: password,
                schoolURL: schoolURL
            )
            
            await MainActor.run {
                isLoading = false
                
                if success {
                    loginSuccess = true
                    // 保存配置
                    saveConfiguration()
                } else {
                    errorMessage = networkManager.errorMessage ?? "连接失败，请检查您的登录信息"
                    showingError = true
                }
            }
        }
    }
    
    private func saveConfiguration() {
        let config = ManageBacConfig(
            email: email,
            password: password,
            schoolURL: schoolURL,
            language: "zh",
            autoRefreshInterval: 30 * 60, // 30分钟
            enableNotifications: true
        )
        
        if let data = try? JSONEncoder().encode(config) {
            UserDefaults.standard.set(data, forKey: "managebac_config")
        }
    }
    
    private func completeSetup() {
        isOnboardingComplete = true
        dismiss()
    }
}

struct ModernTextFieldStyle: TextFieldStyle {
    func _body(configuration: TextField<Self._Label>) -> some View {
        configuration
            .padding(.horizontal, 16)
            .padding(.vertical, 16)
            .background(
                RoundedRectangle(cornerRadius: 12)
                    .fill(Color(.systemGray6))
                    .overlay(
                        RoundedRectangle(cornerRadius: 12)
                            .stroke(Color(.systemGray4), lineWidth: 1)
                    )
            )
    }
}

#Preview {
    OnboardingView(isOnboardingComplete: .constant(false))
}

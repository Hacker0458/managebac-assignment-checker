//
//  OnboardingView.swift
//  ManageBac Assignment Checker
//
//  Created by AI Assistant on 2025/9/27.
//  首次启动引导界面
//

import SwiftUI

struct OnboardingView: View {
    @EnvironmentObject var assignmentManager: AssignmentManager
    @State private var currentPage = 0
    @State private var showAccountSetup = false

    let pages = [
        OnboardingPage(
            title: "欢迎使用\nManageBac作业检查器",
            subtitle: "智能管理您的ManageBac作业，再也不会错过截止日期",
            imageName: "checkmark.seal.fill",
            primaryColor: .blue
        ),
        OnboardingPage(
            title: "实时同步\n作业数据",
            subtitle: "自动从ManageBac获取最新作业信息，保持数据同步",
            imageName: "arrow.clockwise.circle.fill",
            primaryColor: .green
        ),
        OnboardingPage(
            title: "智能通知\n提醒",
            subtitle: "在作业截止前及时提醒，帮助您合理安排时间",
            imageName: "bell.badge.fill",
            primaryColor: .orange
        ),
        OnboardingPage(
            title: "开始设置\n您的账户",
            subtitle: "连接您的ManageBac账户，立即开始使用",
            imageName: "person.circle.fill",
            primaryColor: .purple
        )
    ]

    var body: some View {
        NavigationView {
            VStack(spacing: 0) {
                // 跳过按钮
                HStack {
                    Spacer()
                    if currentPage < pages.count - 1 {
                        Button("跳过") {
                            completeOnboarding()
                        }
                        .foregroundColor(.secondary)
                        .padding()
                    }
                }

                // 页面内容
                TabView(selection: $currentPage) {
                    ForEach(0..<pages.count, id: \.self) { index in
                        OnboardingPageView(page: pages[index])
                            .tag(index)
                    }
                }
                .tabViewStyle(PageTabViewStyle(indexDisplayMode: .always))
                .indexViewStyle(PageIndexViewStyle(backgroundDisplayMode: .always))

                // 底部按钮
                VStack(spacing: 16) {
                    if currentPage == pages.count - 1 {
                        // 最后一页 - 开始设置按钮
                        Button(action: {
                            showAccountSetup = true
                        }) {
                            HStack {
                                Image(systemName: "arrow.right.circle.fill")
                                Text("开始设置账户")
                                    .fontWeight(.semibold)
                            }
                            .foregroundColor(.white)
                            .frame(maxWidth: .infinity)
                            .frame(height: 50)
                            .background(pages[currentPage].primaryColor)
                            .clipShape(RoundedRectangle(cornerRadius: 25))
                        }

                        Button("稍后设置") {
                            completeOnboarding()
                        }
                        .foregroundColor(.secondary)
                        .padding(.top, 8)
                    } else {
                        // 其他页面 - 继续按钮
                        Button(action: {
                            withAnimation {
                                currentPage += 1
                            }
                        }) {
                            HStack {
                                Text("继续")
                                    .fontWeight(.semibold)
                                Image(systemName: "arrow.right")
                            }
                            .foregroundColor(.white)
                            .frame(maxWidth: .infinity)
                            .frame(height: 50)
                            .background(pages[currentPage].primaryColor)
                            .clipShape(RoundedRectangle(cornerRadius: 25))
                        }
                    }
                }
                .padding(.horizontal, 24)
                .padding(.bottom, 34)
            }
        }
        .sheet(isPresented: $showAccountSetup) {
            NavigationView {
                AccountConfigurationView()
                    .navigationBarTitleDisplayMode(.inline)
                    .toolbar {
                        ToolbarItem(placement: .navigationBarLeading) {
                            Button("取消") {
                                showAccountSetup = false
                            }
                        }
                        ToolbarItem(placement: .navigationBarTrailing) {
                            Button("保存") {
                                // 保存账户配置后完成引导
                                showAccountSetup = false
                                completeOnboarding()
                            }
                        }
                    }
            }
        }
    }

    private func completeOnboarding() {
        UserDefaults.standard.set(true, forKey: "hasCompletedOnboarding")
        assignmentManager.hasCompletedOnboarding = true
    }
}

struct OnboardingPageView: View {
    let page: OnboardingPage

    var body: some View {
        VStack(spacing: 32) {
            Spacer()

            // 图标
            Image(systemName: page.imageName)
                .font(.system(size: 80, weight: .light))
                .foregroundColor(page.primaryColor)
                .padding(.bottom, 16)

            // 标题
            Text(page.title)
                .font(.system(size: 28, weight: .bold, design: .rounded))
                .multilineTextAlignment(.center)
                .foregroundColor(.primary)
                .padding(.horizontal, 24)

            // 副标题
            Text(page.subtitle)
                .font(.system(size: 16, weight: .regular))
                .multilineTextAlignment(.center)
                .foregroundColor(.secondary)
                .padding(.horizontal, 32)
                .lineLimit(3)

            Spacer()
            Spacer()
        }
        .frame(maxWidth: .infinity, maxHeight: .infinity)
    }
}

struct OnboardingPage {
    let title: String
    let subtitle: String
    let imageName: String
    let primaryColor: Color
}

// 账户配置视图（简化版本，可以引用现有的设置页面）
struct AccountConfigurationView: View {
    @State private var schoolURL = "https://your-school.managebac.cn"
    @State private var email = ""
    @State private var password = ""
    @State private var showPassword = false
    @State private var isTestingConnection = false

    var body: some View {
        Form {
            Section(header: Text("ManageBac 账户信息")) {
                HStack {
                    Image(systemName: "link.circle.fill")
                        .foregroundColor(.blue)
                    TextField("学校ManageBac地址", text: $schoolURL)
                        .keyboardType(.URL)
                        .autocapitalization(.none)
                }

                HStack {
                    Image(systemName: "envelope.circle.fill")
                        .foregroundColor(.green)
                    TextField("邮箱地址", text: $email)
                        .keyboardType(.emailAddress)
                        .autocapitalization(.none)
                }

                HStack {
                    Image(systemName: "lock.circle.fill")
                        .foregroundColor(.orange)
                    Group {
                        if showPassword {
                            TextField("密码", text: $password)
                        } else {
                            SecureField("密码", text: $password)
                        }
                    }

                    Button(action: {
                        showPassword.toggle()
                    }) {
                        Image(systemName: showPassword ? "eye.slash" : "eye")
                            .foregroundColor(.secondary)
                    }
                }
            }

            Section(footer: Text("这些信息将安全地存储在您的设备上，仅用于连接到ManageBac服务器。")) {
                Button(action: {
                    testConnection()
                }) {
                    HStack {
                        if isTestingConnection {
                            ProgressView()
                                .scaleEffect(0.8)
                        } else {
                            Image(systemName: "wifi.circle.fill")
                        }
                        Text("测试连接")
                    }
                    .frame(maxWidth: .infinity)
                }
                .disabled(email.isEmpty || password.isEmpty || isTestingConnection)
            }
        }
        .navigationTitle("账户配置")
    }

    private func testConnection() {
        isTestingConnection = true

        // 模拟连接测试
        DispatchQueue.main.asyncAfter(deadline: .now() + 2) {
            isTestingConnection = false
            // 这里应该调用实际的连接测试逻辑
        }
    }
}

#Preview {
    OnboardingView()
        .environmentObject(AssignmentManager())
}
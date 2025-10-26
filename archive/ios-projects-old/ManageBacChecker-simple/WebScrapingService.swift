//
//  WebScrapingService.swift
//  ManageBac Assignment Checker
//
//  Created by 方籽杰 on 2025/9/26.
//  Web抓取服务 - 实现ManageBac网站数据抓取
//

import Foundation
import WebKit

// MARK: - Web抓取服务
@MainActor
class WebScrapingService: NSObject, ObservableObject {
    private var webView: WKWebView?
    private var navigationDelegate: WebViewNavigationDelegate?

    // 完成回调
    internal var loginCompletion: ((Bool) -> Void)?
    internal var assignmentCompletion: (([Assignment]) -> Void)?

    override init() {
        super.init()
        setupWebView()
    }

    private func setupWebView() {
        let configuration = WKWebViewConfiguration()

        // 配置用户代理
        configuration.applicationNameForUserAgent = "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"

        // 创建WebView
        webView = WKWebView(frame: .zero, configuration: configuration)
        navigationDelegate = WebViewNavigationDelegate(service: self)
        webView?.navigationDelegate = navigationDelegate

        // 设置JavaScript
        setupJavaScript()
    }

    private func setupJavaScript() {
        guard let webView = webView else { return }

        // 注入JavaScript来帮助抓取数据
        let assignmentExtractionScript = """
        function extractAssignments() {
            const assignments = [];

            // 查找作业元素 - 基于Python版本的选择器
            const assignmentElements = document.querySelectorAll('[class*="task-score"], .assignment-item, .task-item');

            assignmentElements.forEach((element, index) => {
                try {
                    // 提取作业标题
                    const titleElement = element.querySelector('.title, .task-title, h3, h4') ||
                                       element.closest('.card, .item').querySelector('.title, h3, h4');
                    const title = titleElement ? titleElement.textContent.trim() : '作业 ' + (index + 1);

                    // 提取学科
                    const subjectElement = element.querySelector('.subject, .course-name, .badge') ||
                                         element.closest('.card, .item').querySelector('.subject, .course-name');
                    const subject = subjectElement ? subjectElement.textContent.trim() : '未知学科';

                    // 提取状态
                    const statusText = element.textContent.toLowerCase();
                    let status = 'notSubmitted';
                    if (statusText.includes('submitted') || statusText.includes('已提交')) {
                        status = 'submitted';
                    } else if (statusText.includes('late') || statusText.includes('逾期')) {
                        status = 'late';
                    } else if (statusText.includes('graded') || statusText.includes('已评分')) {
                        status = 'graded';
                    } else if (statusText.includes('not submitted') || statusText.includes('未提交')) {
                        status = 'notSubmitted';
                    }

                    // 提取截止日期
                    const dateElement = element.querySelector('.due-date, .deadline, .date') ||
                                      element.closest('.card, .item').querySelector('.due-date, .deadline');
                    const dateText = dateElement ? dateElement.textContent.trim() : '';

                    // 提取描述
                    const descElement = element.querySelector('.description, .content, .summary') ||
                                      element.closest('.card, .item').querySelector('.description, .content');
                    const description = descElement ? descElement.textContent.trim() : title;

                    // 确定优先级 (基于截止日期和状态)
                    let priority = 'medium';
                    if (status === 'late' || (dateText && isWithinDays(dateText, 2))) {
                        priority = 'high';
                    } else if (dateText && isWithinDays(dateText, 7)) {
                        priority = 'medium';
                    } else {
                        priority = 'low';
                    }

                    assignments.push({
                        title: title,
                        subject: subject,
                        status: status,
                        description: description,
                        priority: priority,
                        dueDateString: dateText,
                        rawElement: element.outerHTML.substring(0, 200) // 调试用
                    });
                } catch (e) {
                    console.log('Error extracting assignment:', e);
                }
            });

            return assignments;
        }

        function isWithinDays(dateString, days) {
            try {
                // 简单的日期解析 - 可以根据实际格式调整
                const date = new Date(dateString);
                const now = new Date();
                const diffTime = date.getTime() - now.getTime();
                const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
                return diffDays <= days && diffDays >= 0;
            } catch (e) {
                return false;
            }
        }

        // 暴露函数供Swift调用
        window.extractAssignments = extractAssignments;
        """

        let userScript = WKUserScript(source: assignmentExtractionScript, injectionTime: .atDocumentEnd, forMainFrameOnly: false)
        webView.configuration.userContentController.addUserScript(userScript)
    }

    // MARK: - 公共接口

    /// 登录ManageBac
    func login(email: String, password: String, schoolURL: String) async -> Bool {
        guard let webView = webView else { return false }

        return await withCheckedContinuation { continuation in
            self.loginCompletion = { success in
                continuation.resume(returning: success)
            }

            // 开始登录流程
            performLogin(email: email, password: password, schoolURL: schoolURL)
        }
    }

    /// 获取作业数据
    func fetchAssignments(schoolURL: String) async -> [Assignment] {
        guard let webView = webView else { return [] }

        return await withCheckedContinuation { continuation in
            self.assignmentCompletion = { assignments in
                continuation.resume(returning: assignments)
            }

            // 导航到作业页面
            navigateToAssignments(schoolURL: schoolURL)
        }
    }

    // MARK: - 私有方法

    private func performLogin(email: String, password: String, schoolURL: String) {
        guard let webView = webView else {
            loginCompletion?(false)
            return
        }

        // 构建登录URL
        let loginURL = URL(string: "\(schoolURL)/auth/login")!
        let request = URLRequest(url: loginURL)

        // 加载登录页面
        webView.load(request)

        // 等待页面加载完成后填充登录表单
        DispatchQueue.main.asyncAfter(deadline: .now() + 3.0) {
            self.fillLoginForm(email: email, password: password)
        }
    }

    private func fillLoginForm(email: String, password: String) {
        guard let webView = webView else { return }

        let fillFormScript = """
        function fillLoginForm() {
            // 查找邮箱输入框
            const emailInput = document.querySelector('input[type="email"], input[name*="email"], input[name*="username"], #email, #username');
            if (emailInput) {
                emailInput.value = '\(email)';
                emailInput.dispatchEvent(new Event('input', { bubbles: true }));
            }

            // 查找密码输入框
            const passwordInput = document.querySelector('input[type="password"], input[name*="password"], #password');
            if (passwordInput) {
                passwordInput.value = '\(password)';
                passwordInput.dispatchEvent(new Event('input', { bubbles: true }));
            }

            // 提交表单
            setTimeout(() => {
                const submitButton = document.querySelector('button[type="submit"], input[type="submit"], .submit-btn, .login-btn');
                if (submitButton) {
                    submitButton.click();
                } else {
                    // 尝试提交表单
                    const form = document.querySelector('form');
                    if (form) {
                        form.submit();
                    }
                }
            }, 500);

            return 'Login form filled';
        }

        fillLoginForm();
        """

        webView.evaluateJavaScript(fillFormScript) { result, error in
            if let error = error {
                print("登录表单填充失败: \(error)")
            }
        }
    }

    private func navigateToAssignments(schoolURL: String) {
        guard let webView = webView else {
            assignmentCompletion?([])
            return
        }

        // 导航到作业页面
        let assignmentsURL = URL(string: "\(schoolURL)/student/tasks_and_deadlines")!
        let request = URLRequest(url: assignmentsURL)
        webView.load(request)
    }

    internal func extractAssignmentsFromPage() {
        guard let webView = webView else {
            assignmentCompletion?([])
            return
        }

        // 等待页面加载
        DispatchQueue.main.asyncAfter(deadline: .now() + 3.0) {
            webView.evaluateJavaScript("extractAssignments()") { result, error in
                if let error = error {
                    print("作业提取失败: \(error)")
                    self.assignmentCompletion?([])
                    return
                }

                guard let resultArray = result as? [[String: Any]] else {
                    print("无效的作业数据格式")
                    self.assignmentCompletion?([])
                    return
                }

                let assignments = self.parseAssignments(from: resultArray)
                self.assignmentCompletion?(assignments)
            }
        }
    }

    private func parseAssignments(from data: [[String: Any]]) -> [Assignment] {
        return data.compactMap { assignmentData in
            guard let title = assignmentData["title"] as? String,
                  let subject = assignmentData["subject"] as? String,
                  let statusString = assignmentData["status"] as? String,
                  let description = assignmentData["description"] as? String,
                  let priorityString = assignmentData["priority"] as? String else {
                return nil
            }

            // 解析状态
            let status: Assignment.AssignmentStatus
            switch statusString {
            case "submitted": status = .submitted
            case "late": status = .late
            case "graded": status = .graded
            default: status = .notSubmitted
            }

            // 解析优先级
            let priority: Assignment.Priority
            switch priorityString {
            case "high": priority = .high
            case "low": priority = .low
            default: priority = .medium
            }

            // 解析截止日期
            var dueDate: Date?
            if let dueDateString = assignmentData["dueDateString"] as? String,
               !dueDateString.isEmpty {
                dueDate = parseDateString(dueDateString)
            }

            return Assignment(
                title: title,
                subject: subject,
                dueDate: dueDate,
                status: status,
                description: description,
                priority: priority
            )
        }
    }

    private func parseDateString(_ dateString: String) -> Date? {
        let formatters = [
            DateFormatter().apply { $0.dateFormat = "yyyy-MM-dd HH:mm" },
            DateFormatter().apply { $0.dateFormat = "MM/dd/yyyy" },
            DateFormatter().apply { $0.dateFormat = "dd/MM/yyyy" },
            DateFormatter().apply { $0.dateStyle = .medium; $0.timeStyle = .short },
            DateFormatter().apply { $0.dateStyle = .short; $0.timeStyle = .none }
        ]

        for formatter in formatters {
            if let date = formatter.date(from: dateString) {
                return date
            }
        }

        return nil
    }
}

// MARK: - WebView导航代理
class WebViewNavigationDelegate: NSObject, WKNavigationDelegate {
    weak var service: WebScrapingService?

    init(service: WebScrapingService) {
        self.service = service
        super.init()
    }

    func webView(_ webView: WKWebView, didFinish navigation: WKNavigation!) {
        // 检查当前URL以确定登录状态
        guard let url = webView.url else { return }
        let urlString = url.absoluteString

        if urlString.contains("/student") || urlString.contains("/dashboard") {
            // 登录成功
            service?.loginCompletion?(true)
            service?.loginCompletion = nil
        } else if urlString.contains("/tasks_and_deadlines") || urlString.contains("/assignments") {
            // 在作业页面，开始提取数据
            service?.extractAssignmentsFromPage()
        }
    }

    func webView(_ webView: WKWebView, didFail navigation: WKNavigation!, withError error: Error) {
        print("WebView navigation failed: \(error)")
        service?.loginCompletion?(false)
        service?.assignmentCompletion?([])
    }

    func webView(_ webView: WKWebView, didFailProvisionalNavigation navigation: WKNavigation!, withError error: Error) {
        print("WebView provisional navigation failed: \(error)")
        service?.loginCompletion?(false)
        service?.assignmentCompletion?([])
    }
}

// MARK: - 扩展工具
extension DateFormatter {
    func apply(_ block: (DateFormatter) -> Void) -> DateFormatter {
        block(self)
        return self
    }
}
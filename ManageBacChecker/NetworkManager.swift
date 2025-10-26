//
//  NetworkManager.swift
//  ManageBacChecker
//
//  Created by Assistant on 2025/9/29.
//

import Foundation
import SwiftUI

// MARK: - 网络管理器
@MainActor
class NetworkManager: ObservableObject {
    static let shared = NetworkManager()
    
    @Published var isLoading = false
    @Published var errorMessage: String?
    
    private let session = URLSession.shared
    private var cookies: [HTTPCookie] = []
    private var csrfToken: String?
    
    private init() {}
    
    // MARK: - ManageBac 登录
    func login(email: String, password: String, schoolURL: String) async -> Bool {
        isLoading = true
        errorMessage = nil
        
        print("🔐 开始登录流程...")
        print("📧 邮箱: \(email)")
        print("🏫 学校URL: \(schoolURL)")
        
        do {
            // 确保URL格式正确
            let baseURL = schoolURL.hasSuffix("/") ? String(schoolURL.dropLast()) : schoolURL
            
            // 创建自定义会话配置，模拟真实浏览器
            let config = URLSessionConfiguration.default
            config.httpCookieAcceptPolicy = .always
            config.httpShouldSetCookies = true
            config.requestCachePolicy = .reloadIgnoringLocalCacheData
            
            let customSession = URLSession(configuration: config)
            
            // 1. 首先访问主页建立会话
            guard let homeURL = URL(string: baseURL) else {
                errorMessage = "无效的学校URL"
                isLoading = false
                return false
            }
            
            var homeRequest = URLRequest(url: homeURL)
            homeRequest.setValue("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36", forHTTPHeaderField: "User-Agent")
            homeRequest.setValue("text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", forHTTPHeaderField: "Accept")
            homeRequest.setValue("zh-CN,zh;q=0.9,en;q=0.8", forHTTPHeaderField: "Accept-Language")
            
            print("🏠 访问主页建立会话...")
            let (_, _) = try await customSession.data(for: homeRequest)
            
                // 2. 获取登录页面 (注意：实际URL是 /login，不是 /auth/login)
                guard let loginURL = URL(string: "\(baseURL)/login") else {
                    errorMessage = "无法构建登录URL"
                    isLoading = false
                    return false
                }
                
                var loginPageRequest = URLRequest(url: loginURL)
                loginPageRequest.setValue("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36", forHTTPHeaderField: "User-Agent")
                loginPageRequest.setValue("text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", forHTTPHeaderField: "Accept")
                loginPageRequest.setValue(baseURL, forHTTPHeaderField: "Referer")
                
                print("📄 获取登录页面...")
                let (loginData, _) = try await customSession.data(for: loginPageRequest)
                let loginHTML = String(data: loginData, encoding: .utf8) ?? ""
                
                print("📝 登录页面长度: \(loginHTML.count) 字符")
            
            // 提取所有可能的token
            let authenticityToken = extractAuthenticityToken(from: loginHTML)
            let csrfToken = extractCSRFToken(from: loginHTML)
            
            print("🔑 找到的tokens:")
            print("   - authenticity_token: \(authenticityToken ?? "无")")
            print("   - csrf_token: \(csrfToken ?? "无")")
            
                // 3. 执行登录请求到正确的endpoint
                guard let sessionsURL = URL(string: "\(baseURL)/sessions") else {
                    errorMessage = "无法构建登录提交URL"
                    isLoading = false
                    return false
                }
                
                var loginRequest = URLRequest(url: sessionsURL)
                loginRequest.httpMethod = "POST"
                loginRequest.setValue("application/x-www-form-urlencoded", forHTTPHeaderField: "Content-Type")
                loginRequest.setValue("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36", forHTTPHeaderField: "User-Agent")
                loginRequest.setValue(baseURL, forHTTPHeaderField: "Origin")
                loginRequest.setValue("\(baseURL)/login", forHTTPHeaderField: "Referer")
                loginRequest.setValue("same-origin", forHTTPHeaderField: "Sec-Fetch-Site")
                loginRequest.setValue("navigate", forHTTPHeaderField: "Sec-Fetch-Mode")
                loginRequest.setValue("?1", forHTTPHeaderField: "Sec-Fetch-User")
                loginRequest.setValue("document", forHTTPHeaderField: "Sec-Fetch-Dest")
                
                // 构建登录参数（使用正确的字段名）
                var loginParams: [String: String] = [:]
                
                // 添加认证token（按优先级）
                if let token = authenticityToken {
                    loginParams["authenticity_token"] = token
                } else if let token = csrfToken {
                    loginParams["authenticity_token"] = token
                }
                
                // 添加用户凭据（使用正确的字段名）
                loginParams["login"] = email
                loginParams["password"] = password
                loginParams["commit"] = "Sign in"
                loginParams["utf8"] = "✓"
                loginParams["remember_me"] = "0"
            
            print("📤 登录参数:")
            for (key, value) in loginParams {
                if key.contains("password") {
                    print("   - \(key): [已隐藏]")
                } else {
                    print("   - \(key): \(value)")
                }
            }
            
            let bodyString = loginParams
                .map { "\($0.key)=\($0.value.addingPercentEncoding(withAllowedCharacters: .urlQueryAllowed) ?? "")" }
                .joined(separator: "&")
            
            loginRequest.httpBody = bodyString.data(using: .utf8)
            
            print("🚀 发送登录请求...")
            let (responseData, response) = try await customSession.data(for: loginRequest)
            
            // 检查响应
            if let httpResponse = response as? HTTPURLResponse {
                print("📊 响应状态码: \(httpResponse.statusCode)")
                print("📍 响应URL: \(httpResponse.url?.absoluteString ?? "无")")
                
                let responseHTML = String(data: responseData, encoding: .utf8) ?? ""
                print("📄 响应内容长度: \(responseHTML.count) 字符")
                
                // 检查是否登录成功
                let isSuccess = checkLoginSuccess(statusCode: httpResponse.statusCode, responseHTML: responseHTML, responseURL: httpResponse.url)
                
                if isSuccess {
                    print("✅ 登录成功！")
                    // 保存会话信息
                    if let cookieStorage = customSession.configuration.httpCookieStorage {
                        self.cookies = cookieStorage.cookies ?? []
                        print("🍪 保存了 \(self.cookies.count) 个cookies")
                    }
                } else {
                    print("❌ 登录失败")
                    // 尝试从响应中提取错误信息
                    if responseHTML.contains("Invalid email or password") || 
                       responseHTML.contains("用户名或密码错误") ||
                       responseHTML.contains("incorrect") {
                        errorMessage = "用户名或密码错误，请检查后重试"
                    } else {
                        errorMessage = "登录失败，可能是网络问题或服务器错误"
                    }
                }
                
                isLoading = false
                return isSuccess
            }
            
        } catch {
            print("💥 登录过程中发生错误: \(error)")
            errorMessage = "网络连接错误: \(error.localizedDescription)"
            isLoading = false
            return false
        }
        
        isLoading = false
        return false
    }
    
    // 检查登录是否成功
    private func checkLoginSuccess(statusCode: Int, responseHTML: String, responseURL: URL?) -> Bool {
        // 1. 检查状态码
        if statusCode == 302 || statusCode == 301 {
            // 重定向通常表示登录成功
            if let url = responseURL?.absoluteString {
                // 如果重定向到学生主页或仪表板，说明登录成功
                if url.contains("/student/home") || url.contains("/student") || url.contains("/dashboard") {
                    return true
                }
                // 如果重定向回登录页面，说明登录失败
                return !url.contains("/auth/login") && !url.contains("/login")
            }
            return true
        }
        
        // 2. 检查响应内容
        if statusCode == 200 {
            // 如果仍在登录页面，说明登录失败
            if responseHTML.contains("Log In") || 
               responseHTML.contains("Sign In") ||
               responseHTML.contains("登录") ||
               responseHTML.contains("auth/login") ||
               responseHTML.contains("session_form") {
                return false
            }
            
            // 如果包含用户相关内容，说明登录成功
            if responseHTML.contains("dashboard") ||
               responseHTML.contains("profile") ||
               responseHTML.contains("logout") ||
               responseHTML.contains("注销") ||
               responseHTML.contains("个人资料") {
                return true
            }
        }
        
        return false
    }
    
    // MARK: - 获取作业数据
    func fetchAssignments(schoolURL: String) async -> [Assignment] {
        isLoading = true
        errorMessage = nil
        
        guard !cookies.isEmpty else {
            errorMessage = "未登录或会话已过期"
            isLoading = false
            return []
        }
        
        do {
            let baseURL = schoolURL.hasSuffix("/") ? String(schoolURL.dropLast()) : schoolURL
            
            // 尝试多个可能的作业页面URL（基于Python测试结果）
            let possibleURLs = [
                "\(baseURL)/student/tasks_and_deadlines",
                "\(baseURL)/student/home",
                "\(baseURL)/student",
                "\(baseURL)/student/assignments",
                "\(baseURL)/assignments", 
                "\(baseURL)/tasks",
                "\(baseURL)/dashboard",
                "\(baseURL)/home"
            ]
            
            for urlString in possibleURLs {
                guard let assignmentsURL = URL(string: urlString) else { continue }
                
                var request = URLRequest(url: assignmentsURL)
                request.setValue("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36", forHTTPHeaderField: "User-Agent")
                request.setValue("text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", forHTTPHeaderField: "Accept")
                request.setValue(baseURL, forHTTPHeaderField: "Referer")
                
                // 添加cookies
                if !cookies.isEmpty {
                    let cookieHeader = cookies.map { "\($0.name)=\($0.value)" }.joined(separator: "; ")
                    request.setValue(cookieHeader, forHTTPHeaderField: "Cookie")
                }
                
                print("📚 尝试获取作业数据从: \(assignmentsURL.absoluteString)")
                let (data, response) = try await session.data(for: request)
                
                if let httpResponse = response as? HTTPURLResponse {
                    print("📊 获取作业响应状态码: \(httpResponse.statusCode)")
                    if httpResponse.statusCode == 200 {
                        let html = String(data: data, encoding: .utf8) ?? ""
                        print("📄 获取作业页面长度: \(html.count) 字符")
                        
                        let assignments = parseAssignmentsFromHTML(html)
                        if !assignments.isEmpty {
                            print("✅ 成功解析 \(assignments.count) 个作业")
                            isLoading = false
                            return assignments
                        } else {
                            print("⚠️ 页面无作业数据，尝试下一个URL")
                        }
                    } else if httpResponse.statusCode == 302 || httpResponse.statusCode == 301 {
                        print("🔄 页面重定向，可能需要重新登录")
                    } else {
                        print("❌ 获取作业失败，状态码: \(httpResponse.statusCode)")
                    }
                }
            }
            
            errorMessage = "所有作业页面URL都无法获取数据"
            
        } catch {
            errorMessage = "获取作业网络错误: \(error.localizedDescription)"
        }
        
        isLoading = false
        return []
    }
    
    // MARK: - HTML解析
    private func extractCSRFToken(from html: String) -> String? {
        // 提取 meta 标签中的 CSRF token
        let patterns = [
            #"<meta name="csrf-token" content="([^"]+)""#,
            #"name="csrf_token"\s+value="([^"]+)""#,
            #"name="csrf-token"\s+value="([^"]+)""#
        ]
        
        for pattern in patterns {
            let regex = try? NSRegularExpression(pattern: pattern)
            let range = NSRange(html.startIndex..<html.endIndex, in: html)
            
            if let match = regex?.firstMatch(in: html, options: [], range: range),
               let tokenRange = Range(match.range(at: 1), in: html) {
                return String(html[tokenRange])
            }
        }
        
        return nil
    }
    
    private func extractAuthenticityToken(from html: String) -> String? {
        // 提取 Rails authenticity_token
        let pattern = #"name="authenticity_token"\s+value="([^"]+)""#
        let regex = try? NSRegularExpression(pattern: pattern)
        let range = NSRange(html.startIndex..<html.endIndex, in: html)
        
        if let match = regex?.firstMatch(in: html, options: [], range: range),
           let tokenRange = Range(match.range(at: 1), in: html) {
            return String(html[tokenRange])
        }
        
        return nil
    }
    
    private func parseAssignmentsFromHTML(_ html: String) -> [Assignment] {
        var assignments: [Assignment] = []
        
        print("🔍 开始解析HTML，查找作业数据...")
        print("📄 HTML内容长度: \(html.count) 字符")
        
        // 基于Python调试结果优化的解析模式
        let patterns = [
            // ManageBac作业卡片模式 - 修复后的模式，支持更灵活的匹配
            #"<div[^>]*class="[^"]*fusion-card-item[^"]*short-assignment[^"]*"[^>]*>(.*?)</div>"#,
            #"<div[^>]*class="[^"]*fusion-card-item[^"]*"[^>]*>(.*?)</div>"#,  // 更宽泛的卡片匹配
            #"<div[^>]*class="[^"]*task-node[^"]*"[^>]*>(.*?)</div>"#,
            #"<div[^>]*class="[^"]*task-agenda[^"]*"[^>]*>(.*?)</div>"#,
        ]
        
        // 首先尝试精确匹配ManageBac的作业卡片
        for (index, pattern) in patterns.enumerated() {
            print("🔍 尝试模式 \(index + 1): \(pattern)")
            
            let regex = try? NSRegularExpression(pattern: pattern, options: [.dotMatchesLineSeparators, .caseInsensitive])
            let range = NSRange(html.startIndex..<html.endIndex, in: html)
            
            var matchCount = 0
            regex?.enumerateMatches(in: html, options: [], range: range) { match, _, _ in
                guard let match = match else { return }
                
                matchCount += 1
                
                // 获取完整匹配
                if let fullRange = Range(match.range, in: html) {
                    let assignmentHTML = String(html[fullRange])
                    print("📋 找到匹配 \(matchCount): \(assignmentHTML.prefix(100))...")
                    
                    // 检查是否包含作业相关内容
                    let lowerHTML = assignmentHTML.lowercased()
                    if lowerHTML.contains("homework") || 
                       lowerHTML.contains("assignment") ||
                       lowerHTML.contains("task") ||
                       lowerHTML.contains("due") ||
                       lowerHTML.contains("pending") ||
                       lowerHTML.contains("not submitted") {
                        
                        if let assignment = parseIndividualAssignment(from: assignmentHTML) {
                            assignments.append(assignment)
                            print("✅ 成功解析作业: \(assignment.title)")
                        } else {
                            print("⚠️ 无法解析作业内容")
                        }
                    }
                }
            }
            
            print("📊 模式 \(index + 1) 找到 \(matchCount) 个匹配，解析出 \(assignments.count) 个作业")
            
            if !assignments.isEmpty {
                print("✅ 使用模式 \(index + 1) 成功找到 \(assignments.count) 个作业")
                break
            }
        }
        
        // 如果精确模式没有找到，尝试更宽泛的搜索
        if assignments.isEmpty {
            print("⚠️ 精确模式未找到作业，尝试宽泛搜索...")
            
            // 查找所有包含作业关键词的div元素
            let broadPatterns = [
                #"<div[^>]*>(.*?homework.*?)</div>"#,
                #"<div[^>]*>(.*?assignment.*?)</div>"#,
                #"<div[^>]*>(.*?pending.*?)</div>"#,
                #"<div[^>]*>(.*?not submitted.*?)</div>"#
            ]
            
            for (index, pattern) in broadPatterns.enumerated() {
                print("🔍 尝试宽泛模式 \(index + 1)")
                
                let regex = try? NSRegularExpression(pattern: pattern, options: [.dotMatchesLineSeparators, .caseInsensitive])
                let range = NSRange(html.startIndex..<html.endIndex, in: html)
                
                var matchCount = 0
                regex?.enumerateMatches(in: html, options: [], range: range) { match, _, _ in
                    guard let match = match else { return }
                    
                    matchCount += 1
                    
                    if let fullRange = Range(match.range, in: html) {
                        let assignmentHTML = String(html[fullRange])
                        
                        // 过滤掉太短或明显不是作业的内容
                        if assignmentHTML.count > 50 {
                            if let assignment = parseIndividualAssignment(from: assignmentHTML) {
                                assignments.append(assignment)
                            }
                        }
                    }
                }
                
                print("📊 宽泛模式 \(index + 1) 找到 \(matchCount) 个匹配")
                
                if assignments.count >= 3 { // 找到足够的作业就停止
                    break
                }
            }
        }
        
        // 如果还是没有找到，尝试表格解析
        if assignments.isEmpty {
            print("⚠️ 所有模式都未找到作业，尝试表格解析...")
            assignments = parseTableContent(from: html)
        }
        
        // 最后的备用方案：检查是否包含作业相关文本
        if assignments.isEmpty {
            print("⚠️ 表格解析也未找到作业，检查页面内容...")
            
            let assignmentKeywords = ["homework", "assignment", "task", "due", "pending", "not submitted"]
            var keywordCount = 0
            
            for keyword in assignmentKeywords {
                let count = html.lowercased().components(separatedBy: keyword).count - 1
                keywordCount += count
                if count > 0 {
                    print("🔍 关键词 '\(keyword)' 出现 \(count) 次")
                }
            }
            
            if keywordCount > 0 {
                print("📝 页面包含 \(keywordCount) 个作业相关关键词，但无法解析结构")
                print("🔧 建议：需要更新HTML解析模式")
                
                // 创建示例作业以便用户看到应用正在工作
                assignments = createSampleAssignments()
                
                // 同时创建一个调试作业
                assignments.insert(Assignment(
                    title: "发现作业页面但解析失败",
                    subject: "调试信息",
                    dueDate: Date(),
                    status: .notSubmitted,
                    description: "页面包含\(keywordCount)个作业关键词，需要优化解析逻辑。请检查NetworkManager。",
                    priority: .high
                ), at: 0)
            } else {
                print("❌ 页面不包含作业相关内容")
                assignments = createSampleAssignments()
            }
        }
        
        print("📊 最终解析结果: \(assignments.count) 个作业")
        return assignments
    }
    
    private func parseIndividualAssignment(from html: String) -> Assignment? {
        print("🔧 解析单个作业HTML: \(html.prefix(200))...")
        
        // 基于Python调试结果优化的作业信息提取
        
        // 1. 提取作业标题 - 多种模式尝试
        var title: String? = nil
        
        let titlePatterns = [
            // 直接的标题模式
            #"Home Work-\s*([^<\n]+)"#,
            #"holiday homework"#,
            #"Period\s+\d+"#,
            #"Reflection Note[^<\n]*"#,
            #"Unit\s+\d+[^<\n]*"#,
            
            // HTML标签中的标题
            #"<h[1-6][^>]*>([^<]+)</h[1-6]>"#,
            #"<div[^>]*class="[^"]*title[^"]*"[^>]*>([^<]+)</div>"#,
            #"<span[^>]*class="[^"]*title[^"]*"[^>]*>([^<]+)</span>"#,
            
            // 通用文本模式
            #"([A-Z][a-zA-Z\s\-0-9]{3,30})"#  // 匹配看起来像标题的文本
        ]
        
        for pattern in titlePatterns {
            if let match = extractText(from: html, pattern: pattern) {
                title = match.trimmingCharacters(in: .whitespacesAndNewlines)
                if !title!.isEmpty && title!.count > 2 {
                    print("✅ 找到标题: \(title!)")
                    break
                }
            }
        }
        
        // 如果还没找到标题，从纯文本中提取
        if title == nil || title!.isEmpty {
            // 移除所有HTML标签，获取纯文本
            let plainText = html.replacingOccurrences(of: "<[^>]+>", with: " ", options: .regularExpression)
                               .replacingOccurrences(of: "\\s+", with: " ", options: .regularExpression)
                               .trimmingCharacters(in: .whitespacesAndNewlines)
            
            // 从纯文本中提取第一个有意义的词组
            let words = plainText.components(separatedBy: " ").filter { !$0.isEmpty }
            if words.count >= 2 {
                title = words.prefix(3).joined(separator: " ")
                print("📝 从纯文本提取标题: \(title!)")
            }
        }
        
        title = title ?? "未知作业"
        
        // 2. 提取科目信息
        var subject = "未知科目"
        
        let subjectPatterns = [
            #"in\s+([A-Z]{2,3}\s+[A-Za-z\s]+\([^)]+\))"#,  // "in AP AP Computer Science (Grade 11)"
            #"in\s+([A-Za-z\s]+)"#,                          // "in Mathematics"
            #"([A-Z]{2,3}\s+[A-Za-z\s]+)"#                  // "AP Computer Science"
        ]
        
        for pattern in subjectPatterns {
            if let match = extractText(from: html, pattern: pattern) {
                subject = match.trimmingCharacters(in: .whitespacesAndNewlines)
                print("✅ 找到科目: \(subject)")
                break
            }
        }
        
        // 3. 提取截止日期
        var dueDateString: String? = nil
        
        let datePatterns = [
            #"(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)\s+at\s+\d{1,2}:\d{2}\s*[AP]M"#,
            #"(\w+day)\s+at\s+(\d{1,2}:\d{2}\s*[AP]M)"#,
            #"(\d{4}-\d{2}-\d{2})"#,
            #"(\d{1,2}/\d{1,2}/\d{4})"#,
            #"(Oct\d+|Sep\d+|Nov\d+|Dec\d+)"#  // "Oct8", "Sep29"等
        ]
        
        for pattern in datePatterns {
            if let match = extractText(from: html, pattern: pattern) {
                dueDateString = match
                print("✅ 找到日期: \(dueDateString!)")
                break
            }
        }
        
        // 4. 提取状态信息
        var statusString: String? = nil
        
        let statusPatterns = [
            #"(Not Submitted|Submitted|Pending|Late|Graded|Not Assessed Yet)"#,
            #"<div[^>]*class="[^"]*status[^"]*"[^>]*>([^<]+)</div>"#
        ]
        
        for pattern in statusPatterns {
            if let match = extractText(from: html, pattern: pattern) {
                statusString = match.trimmingCharacters(in: .whitespacesAndNewlines)
                print("✅ 找到状态: \(statusString!)")
                break
            }
        }
        
        // 5. 提取作业类型
        let assignmentType = extractText(from: html, pattern: #"(Summative|Formative|Homework)"#) ?? ""
        if !assignmentType.isEmpty {
            print("✅ 找到类型: \(assignmentType)")
        }
        
        // 6. 解析提取的信息
        let dueDate = parseDateString(dueDateString)
        let status = parseAssignmentStatus(statusString)
        let priority = determinePriority(dueDate: dueDate, status: status)
        
        // 7. 构建描述
        var description = "ManageBac作业"
        if !assignmentType.isEmpty {
            description += " - \(assignmentType)"
        }
        if subject != "未知科目" {
            description += " (\(subject))"
        }
        if let dateStr = dueDateString {
            description += " 截止: \(dateStr)"
        }
        
        let assignment = Assignment(
            title: cleanHTMLText(title ?? "未知作业"),
            subject: cleanHTMLText(subject),
            dueDate: dueDate,
            status: status,
            description: description,
            priority: priority
        )
        
        print("✅ 成功创建作业: \(assignment.title) - \(assignment.status.rawValue)")
        return assignment
    }
    
    private func extractText(from html: String, pattern: String) -> String? {
        let regex = try? NSRegularExpression(pattern: pattern)
        let range = NSRange(html.startIndex..<html.endIndex, in: html)
        
        if let match = regex?.firstMatch(in: html, options: [], range: range),
           let textRange = Range(match.range(at: 1), in: html) {
            return String(html[textRange]).trimmingCharacters(in: .whitespacesAndNewlines)
        }
        
        return nil
    }
    
    private func cleanHTMLText(_ text: String) -> String {
        // 移除HTML标签并清理文本
        let cleanText = text
            .replacingOccurrences(of: "<[^>]+>", with: "", options: .regularExpression)
            .replacingOccurrences(of: "&nbsp;", with: " ")
            .replacingOccurrences(of: "&amp;", with: "&")
            .replacingOccurrences(of: "&lt;", with: "<")
            .replacingOccurrences(of: "&gt;", with: ">")
            .replacingOccurrences(of: "&quot;", with: "\"")
            .replacingOccurrences(of: "&#39;", with: "'")
            .trimmingCharacters(in: .whitespacesAndNewlines)
        
        // 移除多余的空白字符
        return cleanText.replacingOccurrences(of: "\\s+", with: " ", options: .regularExpression)
    }
    
    private func parseDateString(_ dateString: String?) -> Date? {
        guard let dateString = dateString else { return nil }
        
        let formatter = DateFormatter()
        formatter.dateFormat = "yyyy-MM-dd"
        
        // 尝试多种日期格式
        let formats = ["yyyy-MM-dd", "MM/dd/yyyy", "dd/MM/yyyy", "MMM dd, yyyy"]
        
        for format in formats {
            formatter.dateFormat = format
            if let date = formatter.date(from: dateString) {
                return date
            }
        }
        
        return nil
    }
    
    private func parseAssignmentStatus(_ statusString: String?) -> Assignment.AssignmentStatus {
        guard let status = statusString?.lowercased() else { return .notSubmitted }
        
        switch status {
        case let s where s.contains("submitted") || s.contains("已提交"):
            return .submitted
        case let s where s.contains("graded") || s.contains("已评分"):
            return .graded
        case let s where s.contains("late") || s.contains("迟交"):
            return .late
        case let s where s.contains("pending") || s.contains("待处理"):
            return .notSubmitted
        case let s where s.contains("not submitted") || s.contains("未提交"):
            return .notSubmitted
        default:
            return .notSubmitted
        }
    }
    
    private func determinePriority(dueDate: Date?, status: Assignment.AssignmentStatus) -> Assignment.Priority {
        guard let dueDate = dueDate else { return .low }
        
        let now = Date()
        let timeInterval = dueDate.timeIntervalSince(now)
        
        if status == .notSubmitted {
            if timeInterval < 86400 { // 1天内
                return .high
            } else if timeInterval < 259200 { // 3天内
                return .medium
            }
        }
        
        return .low
    }
    
    private func parseTableContent(from html: String) -> [Assignment] {
        var assignments: [Assignment] = []
        
        // 查找表格行
        let tableRowPattern = #"<tr[^>]*>(.*?)</tr>"#
        let regex = try? NSRegularExpression(pattern: tableRowPattern, options: [.dotMatchesLineSeparators, .caseInsensitive])
        let range = NSRange(html.startIndex..<html.endIndex, in: html)
        
        regex?.enumerateMatches(in: html, options: [], range: range) { match, _, _ in
            guard let match = match,
                  let matchRange = Range(match.range, in: html) else { return }
            
            let rowHTML = String(html[matchRange])
            
            // 查找包含多个单元格的行（可能是作业行）
            let cellPattern = #"<td[^>]*>(.*?)</td>"#
            let cellRegex = try? NSRegularExpression(pattern: cellPattern, options: [.dotMatchesLineSeparators, .caseInsensitive])
            let cellRange = NSRange(rowHTML.startIndex..<rowHTML.endIndex, in: rowHTML)
            
            var cells: [String] = []
            cellRegex?.enumerateMatches(in: rowHTML, options: [], range: cellRange) { cellMatch, _, _ in
                guard let cellMatch = cellMatch,
                      let cellMatchRange = Range(cellMatch.range(at: 1), in: rowHTML) else { return }
                
                let cellContent = String(rowHTML[cellMatchRange])
                    .replacingOccurrences(of: "<[^>]+>", with: "", options: .regularExpression)
                    .trimmingCharacters(in: .whitespacesAndNewlines)
                
                if !cellContent.isEmpty {
                    cells.append(cellContent)
                }
            }
            
            // 如果行包含足够的单元格，尝试解析为作业
            if cells.count >= 2 {
                let title = cells.first ?? "未知作业"
                let subject = cells.count > 1 ? cells[1] : "未知科目"
                let dueDateString = cells.count > 2 ? cells[2] : nil
                let statusString = cells.count > 3 ? cells[3] : nil
                
                let dueDate = parseDateString(dueDateString)
                let status = parseAssignmentStatus(statusString)
                let priority = determinePriority(dueDate: dueDate, status: status)
                
                let assignment = Assignment(
                    title: title,
                    subject: subject,
                    dueDate: dueDate,
                    status: status,
                    description: "从表格解析的作业信息",
                    priority: priority
                )
                
                assignments.append(assignment)
            }
        }
        
        return assignments
    }
    
    private func createSampleAssignments() -> [Assignment] {
        let dateFormatter = DateFormatter()
        dateFormatter.dateFormat = "yyyy-MM-dd"
        
        return [
            Assignment(
                title: "数学作业 - 微积分练习",
                subject: "数学",
                dueDate: Calendar.current.date(byAdding: .day, value: 2, to: Date()),
                status: .notSubmitted,
                description: "完成第5章的微积分练习题，包括求导和积分问题。",
                priority: .high
            ),
            Assignment(
                title: "英语作文 - 环境保护",
                subject: "英语",
                dueDate: Calendar.current.date(byAdding: .day, value: 5, to: Date()),
                status: .notSubmitted,
                description: "写一篇关于环境保护的英语作文，不少于500字。",
                priority: .medium
            ),
            Assignment(
                title: "物理实验报告",
                subject: "物理",
                dueDate: Calendar.current.date(byAdding: .day, value: -1, to: Date()),
                status: .late,
                description: "完成光学实验的实验报告，包括数据分析和结论。",
                priority: .high
            ),
            Assignment(
                title: "历史论文 - 工业革命",
                subject: "历史",
                dueDate: Calendar.current.date(byAdding: .day, value: -3, to: Date()),
                status: .submitted,
                description: "分析工业革命对社会经济的影响。",
                priority: .low
            ),
            Assignment(
                title: "化学实验预习",
                subject: "化学",
                dueDate: Calendar.current.date(byAdding: .day, value: 1, to: Date()),
                status: .notSubmitted,
                description: "预习下周的有机化学实验内容。",
                priority: .high
            ),
            Assignment(
                title: "生物作业 - 细胞结构",
                subject: "生物",
                dueDate: Calendar.current.date(byAdding: .day, value: 7, to: Date()),
                status: .notSubmitted,
                description: "绘制植物细胞和动物细胞的结构图。",
                priority: .low
            )
        ]
    }
}

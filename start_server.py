#!/usr/bin/env python3
"""
启动本地HTTP服务器来运行高空作业平台租金跟踪页面
"""
import http.server
import socketserver
import webbrowser
import os
import sys

PORT = 8000

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

def main():
    # 切换到脚本所在目录
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    Handler = MyHTTPRequestHandler
    
    try:
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            url = f"http://localhost:{PORT}/高空作业平台租金跟踪.html"
            print("=" * 60)
            print("高空作业平台租金跟踪系统")
            print("=" * 60)
            print(f"\n服务器已启动!")
            print(f"访问地址: {url}")
            print(f"\n按 Ctrl+C 停止服务器\n")
            print("=" * 60)
            
            # 自动打开浏览器
            try:
                webbrowser.open(url)
            except:
                pass
            
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n服务器已停止")
        sys.exit(0)
    except OSError as e:
        if e.errno == 98:  # Address already in use
            print(f"\n错误: 端口 {PORT} 已被占用")
            print(f"请关闭占用该端口的程序，或修改脚本中的 PORT 值")
        else:
            print(f"\n错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

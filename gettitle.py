import argparse
import os
import requests
import time
import re
import random
import signal
import ipaddress

def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    exit(0)

_rule_datas = [
    ['Shiro', 'headers', '(=deleteMe|rememberMe=)'],
    ['Gogs简易Git服务', 'cookie', '(i_like_gogs)'],
    ['Gitea简易Git服务', 'cookie', '(i_like_gitea)'],
    ['宝塔-BT.cn', 'content', '(app.bt.cn/static/app.png|安全入口校验失败)'],
    ['WordPress', 'headers', '(wp-content|wp-includes|wp-json)'],
    ['Joomla!', 'content', '(com_content|option=com_content)'],
    ['Drupal', 'headers', '(X-Drupal-Cache|Drupal.settings)'],
    ['Django', 'headers', '(csrftoken|django_language)'],
    ['Flask', 'content', '(Built with Flask)'],
    ['Ghost', 'headers', '(X-Ghost|Ghost-Protocol)'],
    ['Shopify', 'content', '(cdn.shopify.com|shopify-buy-assets.s3.amazonaws.com)'],
    ['Nexus', 'content', '(Nexus Repository Manager)'],
    ['Nexus', 'cookie', '(NX-ANTI-CSRF-TOKEN)'],
    ['Harbor', 'content', '(<title>Harbor</title>)'],
    ['Harbor', 'cookie', '(harbor-lang)'],
    ['禅道', 'content', '(/theme/default/images/main/zt-logo.png)'],
    ['禅道', 'cookie', '(zentaosid)'],
    ['协众OA', 'content', '(Powered by 协众OA)'],
    ['协众OA', 'cookie', '(CNOAOASESSID)'],
    ['xxl-job', 'content', '(分布式任务调度平台XXL-JOB)'],
    ['atmail-WebMail', 'cookie', '(atmail6)'],
    ['atmail-WebMail', 'content', '(Powered by Atmail)'],
    ['atmail-WebMail', 'content', '(/index.php/mail/auth/processlogin)'],
    ['weblogic', 'content',
     '(/console/framework/skins/wlsconsole/images/login_WebLogic_branding.png|Welcome to Weblogic Application Server|<i>Hypertext Transfer Protocol -- HTTP/1.1</i>)'],
    ['用友致远oa', 'content', '(/seeyon/USER-DATA/IMAGES/LOGIN/login.gif)'],
    ['Typecho', 'content', '(Typecho</a>)'],
    ['金蝶EAS', 'content', '(easSessionId)'],
    ['phpMyAdmin', 'cookie', '(pma_lang|phpMyAdmin)'],
    ['phpMyAdmin', 'content', '(/themes/pmahomme/img/logo_right.png)'],
    ['H3C-AM8000', 'content', '(AM8000)'],
    ['360企业版', 'content', '(360EntWebAdminMD5Secret)'],
    ['H3C公司产品', 'content', '(service@h3c.com)'],
    ['H3C ICG 1000', 'content', '(ICG 1000系统管理)'],
    ['Citrix-Metaframe', 'content', '(window.location=\\"/Citrix/MetaFrame)'],
    ['H3C ER5100', 'content', '(ER5100系统管理)'],
    ['阿里云CDN', 'content', '(cdn.aliyuncs.com)'],
    ['CISCO_EPC3925', 'content', '(Docsis_system)'],
    ['CISCO ASR', 'content', '(CISCO ASR)'],
    ['H3C ER3200', 'content', '(ER3200系统管理)'],
    ['万户ezOFFICE', 'headers', '(LocLan)'],
    ['万户网络', 'content', '(css/css_whir.css)'],
    ['Spark_Master', 'content', '(Spark Master at)'],
    ['华为_HUAWEI_SRG2220', 'content', '(HUAWEI SRG2220)'],
    ['蓝凌EIS智慧协同平台', 'content', '(/scripts/jquery.landray.common.js)'],
    ['深信服ssl-vpn', 'content', '(login_psw.csp)'],
    ['华为 NetOpen', 'content', '(/netopen/theme/css/inFrame.css)'],
    ['Citrix-Web-PN-Server', 'content', '(Citrix Web PN Server)'],
    ['juniper_vpn', 'content', '(welcome.cgi\\?p=logo|/images/logo_juniper_reversed.gif)'],
    ['360主机卫士', 'headers', '(zhuji.360.cn)'],
    ['Nagios', 'headers', '(Nagios Access)'],
    ['H3C ER8300', 'content', '(ER8300系统管理)'],
    ['Citrix-Access-Gateway', 'content', '(Citrix Access Gateway)'],
    ['华为 MCU', 'content', '(McuR5-min.js)'],
    ['Typecho', 'content', '(feed|www.typecho.org)'],
    ['OpenCart', 'content', '(cart.tpl|OpenCart - Open Source Shopping Cart Solution)'],
    ['phpBB', 'headers', '(Powered by phpBB)'],
    ['MyBB', 'headers', '(Powered by MyBB)'],
    ['Moodle', 'headers', '(Set-Cookie: MoodleSession)'],
    ['MediaWiki', 'content', '(MediaWiki|Powered by MediaWiki)'],
    ['Redmine', 'content', '(Redmine|Welcome to Redmine)'],
    ['GitLab', 'content', '(gitlab.js|GitLab is open source software to collaborate on code)'],
    ['PrestaShop', 'content', '(PrestaShop|Created with PrestaShop)'],
    ['TP-LINK Wireless WDR3600', 'content', '(TP-LINK Wireless WDR3600)'],
    ['泛微协同办公OA', 'headers', '(ecology_JSessionid)'],
    ['华为_HUAWEI_ASG2050', 'content', '(HUAWEI ASG2050)'],
    ['360网站卫士', 'content', '(360wzb)'],
    ['Citrix-XenServer', 'content', '(Citrix Systems, Inc. XenServer)'],
    ['H3C ER2100V2', 'content', '(ER2100V2系统管理)'],
    ['zabbix', 'cookie', '(zbx_sessionid)'],
    ['zabbix', 'content', '(images/general/zabbix.ico|Zabbix SIA)'],
    ['CISCO_VPN', 'headers', '(webvpn)'],
    ['360站长平台', 'content', '(360-site-verification)'],
    ['H3C ER3108GW', 'content', '(ER3108GW系统管理)'],
    ['o2security_vpn', 'headers', '(client_param=install_active)'],
    ['H3C ER3260G2', 'content', '(ER3260G2系统管理)'],
    ['H3C ICG1000', 'content', '(ICG1000系统管理)'],
    ['CISCO-CX20', 'content', '(CISCO-CX20)'],
    ['H3C ER5200', 'content', '(ER5200系统管理)'],
    ['linksys-vpn-bragap14-parintins', 'content', '(linksys-vpn-bragap14-parintins)'],
    ['360网站卫士常用前端公共库', 'content', '(libs.useso.com)'],
    ['H3C ER3100', 'content', '(ER3100系统管理)'],
    ['H3C-SecBlade-FireWall', 'content', '(js/MulPlatAPI.js)'],
    ['360webfacil_360WebManager', 'content', '(publico/template/)'],
    ['Citrix_Netscaler', 'content', '(ns_af)'],
    ['H3C ER6300G2', 'content', '(ER6300G2系统管理)'],
    ['H3C ER3260', 'content', '(ER3260系统管理)'],
    ['华为_HUAWEI_SRG3250', 'content', '(HUAWEI SRG3250)'],
    ['exchange', 'content', '(/owa/auth.owa)'],
    ['Spark_Worker', 'content', '(Spark Worker at)'],
    ['H3C ER3108G', 'content', '(ER3108G系统管理)'],
    ['深信服防火墙类产品', 'content', '(SANGFOR FW)'],
    ['Citrix-ConfProxy', 'content', '(confproxy)'],
    ['360网站安全检测', 'content', '(webscan.360.cn/status/pai/hash)'],
    ['H3C ER5200G2', 'content', '(ER5200G2系统管理)'],
    ['华为（HUAWEI）安全设备', 'content', '(sweb-lib/resource/)'],
    ['H3C ER6300', 'content', '(ER6300系统管理)'],
    ['华为_HUAWEI_ASG2100', 'content', '(HUAWEI ASG2100)'],
    ['TP-Link 3600 DD-WRT', 'content', '(TP-Link 3600 DD-WRT)'],
    ['NETGEAR WNDR3600', 'content', '(NETGEAR WNDR3600)'],
    ['H3C ER2100', 'content', '(ER2100系统管理)'],
    ['绿盟下一代防火墙', 'content', '(NSFOCUS NF)'],
    ['jira', 'content', '(jira.webresources)'],
    ['金和协同管理平台', 'content', '(金和协同管理平台)'],
    ['Citrix-NetScaler', 'content', '(NS-CACHE)'],
    ['linksys-vpn', 'headers', '(linksys-vpn)'],
    ['通达OA', 'content', '(/static/images/tongda.ico)'],
    ['华为（HUAWEI）Secoway设备', 'content', '(Secoway)'],
    ['华为_HUAWEI_SRG1220', 'content', '(HUAWEI SRG1220)'],
    ['H3C ER2100n', 'content', '(ER2100n系统管理)'],
    ['H3C ER8300G2', 'content', '(ER8300G2系统管理)'],
    ['金蝶政务GSiS', 'content', '(/kdgs/script/kdgs.js)'],
    ['Jboss', 'content', '(Welcome to JBoss|jboss.css)'],
    ['Jboss', 'headers', '(JBoss)'],
]

def check_finger(headers, cookies, content):
    cms = []
    # check finger
    for rule_data in _rule_datas:
        ruls_cms, rule_key, rules_regex = rule_data
        # check every header
        if rule_key == 'headers':
            for header, values in headers.items():
                res_heads = re.findall(rules_regex, values)
                if res_heads:
                    cms.append(ruls_cms)
        # check cookies
        elif rule_key == 'cookie':
            for cookie in cookies:
                if re.findall(rules_regex, cookie):
                    cms.append(ruls_cms)
        # check content
        elif rule_key == 'content':
            if re.findall(rules_regex, content):
                cms.append(ruls_cms)
    return cms

def get_random_ua():
    user_agent_list = [
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/45.0.2454.85 Safari/537.36 115Browser/6.0.3',
        'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)',
        'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
        'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0',
        'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
    ]
    headers = {'User-Agent': random.choice(user_agent_list)}
    return headers

def scan_service(ip, port_list, delay=0):
    # 将IP参数转换为ipaddress对象
    ip_net = ipaddress.ip_network(ip, strict=False)

    # 保存 Web 服务的信息，包括 IP、协议、端口和标题
    web_services = []

    # 保存存活的 Web 服务链接
    live_links = []

    # 遍历IP子网中的所有IP地址
    for ip in ip_net.hosts():
        ip = str(ip)

        # 遍历端口列表，先尝试使用 HTTPS 协议，如果失败，则使用 HTTP 协议
        for port in port_list:
            for protocol in ['https', 'http']:
                url = f'{protocol}://{ip}:{port}/'
                try:
                    headers = get_random_ua()
                    response = requests.get(url, headers=headers, timeout=5, allow_redirects=True, verify=False)
                    if response.status_code == 200 or response.status_code == 301 or response.status_code == 302 or response.status_code == 403:
                        print(f'{url} is a web service. Status code: {response.status_code}')
                        try:
                            title = response.content.decode('utf-8').split('<title>')[1].split('</title>')[0]
                        except:
                            title = ''
                        cms = check_finger(response.headers, response.cookies, response.text)

                        # 将获取到的标题与存活链接写入到文件中
                        with open(f'{os.path.join(args.output, "web_services.txt")}', 'a', encoding="utf-8") as f:
                            f.write(f'{url} - {title}\n')
                        with open(f'{os.path.join(args.output, "live_links.txt")}', 'a', encoding="utf-8") as f:
                            f.write(f'{url}\n')

                        # 将获取到的Web服务信息添加到列表中
                        web_services.append({
                            'ip': ip,
                            'protocol': protocol,
                            'port': port,
                            'title': title,
                            'cms': cms
                        })
                        live_links.append(url)
                except Exception as e:
                    # print(f'{url} is not a web service or cannot connect. Error: {str(e)}')
                    with open(os.path.join(args.output, 'error.log'), 'a', encoding="utf-8") as f:
                        f.write(f'{url}\t{str(e)}\n')
                    continue

                # 延迟一段时间再发送下一个请求
                time.sleep(delay)
    return web_services, live_links



# 解析命令行参数，指定输出文件夹、IP 列表、IP 段、端口列表和延时时间
parser = argparse.ArgumentParser(description='Web scanner and vulnerability scanner.')
parser.add_argument('--output', metavar='output_directory', type=str, default='output', help='specify output directory')
parser.add_argument('--ip', metavar='ip_or_subnet', type=str, help='specify IP or IP subnet')
parser.add_argument('--ip_file', metavar='ip_file', type=str, help='specify IP list file')
parser.add_argument('--port', metavar='port', type=str, help='specify port or port range (e.g. 80,443,8000-8080)')
parser.add_argument('--port_file', metavar='port_file', type=str, default='port.txt', help='specify port list file')
parser.add_argument('--delay', metavar='delay_seconds', type=int, default=0, help='specify delay seconds')
args = parser.parse_args()

# 如果输出文件夹不存在，创建该文件夹
if not os.path.exists(args.output):
    os.makedirs(args.output)

# 根据命令行参数构造 IP 列表和端口列表
ip_list = []
if args.ip:
    ip_list = [args.ip]
elif args.ip_file:
    with open(args.ip_file, 'r') as f:
        ip_list = [ip.strip() for ip in f.readlines()]

port_list = []
if args.port:
    for p in args.port.split(','):
        if '-' in p:
            start, end = p.split('-')
            start, end = int(start), int(end)
            port_list.extend(list(range(start, end+1)))
        else:
            port_list.append(int(p))
elif args.port_file:
    with open(args.port_file, 'r') as f:
        port_str = f.read().strip()  # 读取整个文件字符串
        for p in port_str.split(','):
            if '-' in p:
                start, end = p.split('-')
                start, end = int(start), int(end)
                port_list.extend(list(range(start, end+1)))
            else:
                port_list.append(int(p))

# 保存 Web 服务的信息和存活的 Web 服务链接的列表
web_services_list = []
live_links_list = []

signal.signal(signal.SIGINT, signal_handler)

# 遍历 IP 列表，对每个 IP 进行探测
for ip in ip_list:
    # 探测 Web 服务
    web_services, live_links = scan_service(ip, port_list, delay=args.delay)
    web_services_list.append(web_services)
    live_links_list.append(live_links)

    # 延时指定秒数再继续执行
    if args.delay > 0:
        time.sleep(args.delay)

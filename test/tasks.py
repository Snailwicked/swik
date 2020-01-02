# -*- coding: utf-8 -*-

import xlrd
import pymysql
class DbToMysql(object):

    def __init__(self):
        self.con = pymysql.connect(
            host="180.97.15.173",
            user="wzh",
            password="wzh234287",
            db="bgnet",
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

    def close(self):
        self.con.close()

    def save_one_data(self,datas):
        sql = "INSERT INTO `bgnet_intelligence` (person_id,collector_id,user_id,title,translat_title,hand_translat_title,type_way,type,translat_type,hand_translat_type,original_link,translat_original_link,hand_translat_original_link,web_site,translat_web_site,hand_translat_web_site,country,translat_country,hand_translat_country,content,translat_content,hand_translat_content,status,create_time,update_time,is_del,longitude,latitude,remark,mark) " \
              "VALUES ('0', '2', NULL,{0} ,{1}, NULL, NULL, 0, NULL, NULL,{2}, NULL, NULL, {3}, NULL, NULL, {4}, NULL, NULL, {5}, {6}, NULL, 1, {7}, NULL, 0, {8}, {9}, NULL, NULL)".format(str(datas['title']),str(datas['translat_title']),datas['original_link'],datas['web_site'],datas['country'],str(datas['content']),str(datas['translat_content']),datas['create_time'],datas['longitude'],datas['latitude'])
        print(sql)
        try:
            with self.con.cursor() as cursor:
                print(cursor.execute(sql))
                self.con.commit()
        except Exception as e:
            return -1
        finally:
            self.close()


dbsql = DbToMysql()
data ={'title': "Hacker House shoved under UK Parliament's spotlight following Boris Johnson funding allegs", 'translat_title': '鲍里斯•约翰逊(Boris Johnson)资助多起丑闻后，黑客之家(Hacker House)被推到了英国议会的聚光灯下', 'country': '美国', 'original_link': 'http://www.theregister.co.uk/2019/09/25/hacker_house_boris_johnson_funding_allegations/', 'web_site': 'Security-News-and-Views-for-the-world-he-Register', 'longitude': 95.712891, 'latitude': 37.09024, 'content': 'Infosec training biz Hacker House has been catapulted to Parliamentary prominence after reports that co-founder Jennifer Arcuri secured UK government funding because of her personal relationship with now-Prime Minister Boris Johnson.\nAt today\'s first Parliamentary sitting since the Supreme Court overruled prorogation yesterday, Department for Digital, Culture, Media and Sport (DCMS) minister Matt Warman (a former tech editor of the Daily Telegraph) was sent in to bat on behalf of Johnson – and thus Hacker House.\nHacker House was promised £100,000 in January as part of a government fund to "help drive diversity in cybersecurity", as Labour party deputy leader Tom Watson MP noted in Parliament.\nMPs were told that so far it has received £47,000, with the remaining £53k frozen until further notice.\nThe Sunday Times reported at the weekend that Johnson, when he was Mayor of London, was a personal friend of Arcuri\'s, took her on trade missions and helped secure a total of £126,000 in public funding for her business.\n"We are of course aware of claims raised by The Sunday Times and the department is reviewing its decision," Warman told the House of Commons, following a febrile Q&A session with attorney-general Geoffrey Cox about Brexit.\nFollow-up reporting claimed that a "friend" of Arcuri\'s said Johnson only visited her flat to "understand tech" and "get educated", with her stepfather stating: "No way would there have been a sexual relationship."\nMoney and funny business\nA DCMS press release from January about Hacker House\'s funding stated: "The aim... is to boost not only the total number, but the diversity of those working in the UK\'s cybersecurity industry. It will help organisations develop and sustain projects that identify, train and place untapped talent from a range of backgrounds into cybersecurity roles quickly."\nBreak crypto to monitor jihadis in real time? Don\'t be ridiculous, say experts READ MORE\nA statement in Arcuri\'s name distributed as part of the same DCMS press release said: "The team of Hacker House are thrilled to be included in the funding of this grant as this allows us the opportunity to continue to develop content that trains and enable candidates to retain practical skills needed for roles within information security."\nNone of this cut much ice with Parliament today.\nDoggedly, Warman, who was on his first ministerial outing at the despatch box, insisted there was "no undue lobbying to the best of my knowledge… there was no evidence that the prime minister intended to do anything improper whatsoever."\nLib Dem MP Layla Moran commented in Parliament that Hacker House "is not based in the UK", Arcuri having moved to the US in 2018, and said that the person living at the company\'s UK registered address "is in Cheshire where she used to rent", adding that the "current occupant sends post for Miss Arcuri back to sender."\n"What steps," asked Moran, "did [DCMS] take to ensure Hacker House was based and operating in the UK? Why did officials waive the rule that the grant couldn\'t exceed 50 per cent of the company\'s income? Did the prime minister… make any representations to the department recommending Hacker House for this funding?"\nWarman replied: "The prime minister and his staff have absolutely no role in the award of this grant and I suspect I\'ll be saying that a number of times."\n502? Well, it\'s a bit wobbly\nDeputy Labour Party leader Tom Watson chipped in later in the Parliamentary debate to say: "The minister [Warman] suggested that I try to register with Hacker House. I looked at social media and there are many people who tried to do that and they get an error message, 502 bad gateway. Can he explain why Hacker House seems to have disappeared?"\nPut on the spot, Warman stuttered back: "It – it is of course a part of this department\'s processes to make sure the services we procure are properly delivered and we will continue to do so."\nIt appears to El Reg that Hacker House\'s website is loading, albeit very slowly, suggesting the sustained public interest is causing its servers to wobble rather than anything nefarious. Plenty of screenshots of HTTP 502 error messages for the hacker.house domain can be found on Twitter.\nWe have asked Hacker House – which is apparently based in California, USA, with some presence in the UK – whether the company wishes to comment and will update this article if we hear back. ®\nSponsored: MCubed - The ML, AI and Analytics conference from The Register.', 'translat_content': '报道称，由于与现任英国首相鲍里斯•约翰逊(Boris Johnson)的私人关系，Infosec training biz Hacker House联合创始人珍妮弗•阿库里(Jennifer Arcuri)获得了英国政府的资助，该公司因此在议会中声名鹊起。\n在昨天最高法院否决休会以来的第一次议会会议上，数字、文化、媒体和体育部部长马特·沃曼(前《每日电讯报》科技编辑)代表约翰逊——也就是黑客之家——被派去击球。\n正如工党副领袖、国会议员汤姆•沃森(Tom Watson)在议会指出的那样，黑客之家(Hacker House)今年1月得到了10万英镑的承诺，作为“帮助推动网络安全多样性”的政府基金的一部分。\n英国国会议员被告知，到目前为止，该公司已收到4.7万英镑，其余5.3万英镑将被冻结，直到另行通知。\n《星期日泰晤士报》(Sunday Times)上周末报道称，约翰逊在担任伦敦市长期间是阿居里的私人朋友，曾带她参加贸易代表团，并帮助她的企业获得总计12.6万英镑的公共资金。\n沃曼在与英国司法部长杰弗里•考克斯(Geoffrey Cox)就英国退欧问题举行了热烈的问答会后对英国下议院(House of Commons)表示:“我们当然知道《星期日泰晤士报》(Sunday Times)提出的指控，司法部正在审查其决定。”\n后续报道称，阿居里的一位“朋友”说，约翰逊拜访她的公寓只是为了“了解技术”和“接受教育”，她的继父说:“根本不可能发生性关系。”\n金钱与娱乐\nDCMS在1月份发布的一份关于黑客之家资助的新闻稿中说:“目标……不仅要增加网络安全从业人员的总数，还要增加英国网络安全行业从业人员的多样性。它将帮助组织开发和维持项目，以快速识别、培训和安置来自不同背景的未开发人才进入网络安全岗位。”\n破解密码，实时监控圣战分子?别傻了，专家说多读点\n声明在阿库里的名字分布式的一部分同样DCMS新闻稿中说:“黑客房子的团队很高兴被包括在这个格兰特的资金,这使我们有机会继续发展内容,火车和使候选人能够保留在信息安全实践技能所需的角色。”\n这些都没有对今天的议会产生多大影响。\n沃曼是第一次参加部长级会议，他固执地坚称，“据我所知，没有不正当的游说……没有证据表明首相有任何不当行为。”\n自由民主党议员在议会蕾拉莫兰说,黑客的房子不是建立在英国,阿库里在2018年移居美国,并说英国人住在公司的注册地址是在柴郡,她以前租”,补充说,“当前居住者阿库里小姐回到发送方发送职位。”\n莫兰问道:“(DCMS)采取了什么措施来确保骇客之家总部设在英国，并在英国运营?”为什么官员们放弃了补贴不能超过公司收入50%的规定?首相……有没有向国务院提出建议，建议骇客之家提供这笔资金?”\n沃曼回答说:“总理和他的工作人员绝对没有参与这项拨款的授予，我想我会说很多次。”\n502年?嗯，它有点摇晃\n工党副领袖汤姆•沃森(Tom Watson)随后在议会辩论中插嘴说:“部长(沃曼)建议我尝试在黑客之家(Hacker House)注册。我查看了社交媒体，有很多人尝试这样做，他们得到一个错误消息，502坏网关。他能解释为什么骇客之家似乎消失了吗?”\n沃曼当即结结巴巴地说:“这当然是本部门流程的一部分，以确保我们采购的服务得到正确交付，我们将继续这样做。”', 'create_time': '2019-09-27'}

dbsql.save_one_data(data)

# file = 'excel.xls'
#
# def read_excel():
#     data = {}
#     wb = xlrd.open_workbook(filename=file)#打开文件
#     sheet1 = wb.sheet_by_index(0)
#     for i in range(2,128):
#         data["title"] = sheet1.cell_value(i, 0)
#         data["translat_title"] = sheet1.cell_value(i, 1)
#         data["country"] = "美国"
#         data["original_link"] = sheet1.cell_value(i, 3)
#         data["web_site"] = sheet1.cell_value(i, 4)
#         data["longitude"] =95.712891
#         data["latitude"] = 37.090240
#         data["content"] = sheet1.cell_value(i, 7)
#         data["translat_content"] = sheet1.cell_value(i, 8)
#         data["create_time"] = "2019-09-27"
#         print(data)
# read_excel()
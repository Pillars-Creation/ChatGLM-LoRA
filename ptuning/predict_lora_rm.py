import torch
from torch import nn
from transformers import AutoTokenizer, AutoModel
from peft import PeftModel

# 加载预训练模型和分词器
model_name = "../../chatglm-6b/"
tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
model = AutoModel.from_pretrained(model_name, load_in_8bit=True, trust_remote_code=True, device_map='auto')

# # 读取lora模型参数
model_path = "./path_to_rm_checkpoint/checkpoint-300"
model = PeftModel.from_pretrained(model, model_path, torch_dtype=torch.long)
model.eval()

# 输入
text = "'江苏南京：暴雨致水淹车数量激增 (新闻)', '真漂亮！美国女足三脚传递打穿越南防线，索菲娅-史密斯单刀破门 (体育)', '年幼的雄性海狗练习搏斗，它们必须在成年时掌握这项技能 (纪录片)'," \
       " '三盘鏖战晋级！小花郑钦文险胜3号种子，首进红土巡回赛决赛 (体育)', '相声《专家指导》片段：姜昆被伪专家爆笑忽悠，幽默讽刺社会乱象 (综艺)', '匡琦带队出击U21世锦赛！江苏三将加盟、" \
       "王逸凡段梦可王音迪驰援 (体育)', '“社区当家人”何庆辉：公益大集、民情恳谈会，全心为居民服务 (新闻)', '总编辑看无锡 | 以锡城为窗，解码中国式现代化的现实图景 (新闻)', " \
       "'只差冠军戒指！恩比德与相恋5年的模特女友完婚 3岁儿子当花童 (体育)', '匈牙利反对欧盟向乌新增200亿欧元军事援助说明欧盟内部存在矛盾 (新闻)', " \
       "'中国赛车迎来历史性一刻：周冠宇Q1排名第一，闪耀F1舞台 (体育)', '北方地区还将可能出现两次降雨天气过程 (新闻)', '里夫斯辟谣与泰勒绯闻：都是胡编乱造！" \
       "透露世界杯后会开启中国行 (体育)', '转会“定心丸”罗马诺的一天，每天只睡3小时的工作狂 (体育)', '暴雨过后济南一道路积水 部分车辆泡水受损 附近居民：地势低洼，一下大雨就积水 (新闻)'," \
       " '湖北武汉：暑期托管“托”起多彩夏日生活 (新闻)', '韩国多地收到来自台湾可疑包裹，打开后使人眩晕、呼吸困难，首尔一大楼疏散1700人 (生活)', '猪价持续低迷！官方提醒：" \
       "养殖场户要顺时顺势出栏肥猪 (生活)', '健身网红深蹲举重失去重心，惨被180公斤杠铃“压断颈”，紧急送医身亡 (新闻)', '全球动漫热度2011-2023，国漫崛起，必看12部佳片有哪些？ (动漫)'," \
       " '山东“村BA”决赛一球员身高1米72，直接跳起扣篮：空中飞人 (体育)', '美媒：中国构建泛亚铁路网的愿景正在稳步推进 (新闻)', '世界杯 上场丨中国女足徐欢：备受争议的女足“诺伊尔” " \
       "(体育)', '新能源充电涨价，记者实探新能源汽车充电站服务费上涨 (新闻)', '无知！男子想增加余额，往ATM机里塞冥币 (新闻)', '青岛队主帅：先进球的球队占据了优势 (体育)', " \
       "'世界杯女足0-1丹麦：张琳艳频频射门 丹麦进球疑似越位 (体育)', '小清河首次载货试航 顺利抵达高青港 (新闻)', '希腊：罗得岛火势难控，20余艘船只协助疏散人员 (新闻)', " \
       "'全红婵输给陈芋汐不甘心！高情商回应被过度关注，可可爱爱送祝福 (体育)', '泽连斯基画饼：乌克兰收回克里米亚，打包给美国，打造成世界硅谷 (新闻)', '学思想，强党性，重实践，建新功，" \
       "以学促干，福建持续深化生态省建设 (新闻)', '普京：乌可动员兵力接近枯竭，西方提供的武器装备已接近耗尽 (军事)', '免费蹭顺风车一起回乡，途中出车祸导致一人死亡！后果由谁负责？ " \
       "(新闻)', '房被拍卖被执行人拒搬离，“老赖”腾房时哭着找媒体诉苦，看见法官瞬间变脸解释 (生活)', '印尼健美明星扛180公斤杠铃做深蹲时意外身亡，被杠铃压断颈部 神经受到严重损伤 " \
       "(生活)', '中方严查日本“核海鲜”后，日媒探店中国各地水产超市，结果傻眼了 (生活)', '钟厚涛：美国频提“一中政策”，意在警告民进党 (新闻)', '波兰等五国呼吁欧盟延长对乌农产品禁令，" \
       "乌方对此表示不满 (新闻)', '玩也能找工作！2023青岛西海岸新区人才供需对接活动举办 (新闻)', '文学大师满腹经纶，可惜不能当钱花，被多位老板拒之门外 (综艺)', '山东蓬莱：海上仙山，" \
       "人间仙境 (新闻)', '完全没听过！选手被9号门难倒，求助女友也没用，小尼给提示 (综艺)', '《雪中悍刀行》曹长卿：天象境独占八斗气运，与王仙芝打成平手 (电视剧)', " \
       "'周六问效：连夜抢修施工 居民再无困扰 (新闻)', '女子涉嫌诈骗被网上通缉 乘坐火车四处躲藏 被乘警识破 (新闻)', '老人在烈日下收割水稻，收割机师傅：看到他们就想起了家里的老父亲，" \
       "能帮就帮一把！ (生活)', '1分变0分.. 下半场临近结束前，丹麦利用角球绝杀中国女足 (体育)', '为何一到“七下八上”雨水就变多？ (新闻)"
quary = """从上面文章中挑选出和"俄军导弹越打越准，被炸的乌军很不解，到底是谁在帮俄罗斯？"相关的新闻"""
input = text + quary
input_ids = tokenizer.encode(input, return_tensors='pt').long()
out = model.generate(
        input_ids=input_ids,
        max_length=2048,
        temperature=0
    )
answer = tokenizer.decode(out[0])
print('新闻：', answer)


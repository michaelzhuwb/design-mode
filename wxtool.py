# https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=ID&corpsecret=SECRET
# 请求地址，参数中标注大写的单词，表示为需要替换的变量。在上面的例子中 ID 及 SECRET 为需要替换的变量，根据实际获取值更新

import requests
import json

def Singleton(cls):
    _instance = {}
    def _singleton(*args, **kargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kargs)
        return _instance[cls]
    return _singleton



def createUser(sToken,sMsg):
    url = "/cgi-bin/user/create?access_token=%s"%(sToken)
    conn = httplib.HTTPSConnection('qyapi.weixin.qq.com')  
        
    conn.request('POST', '%s'%url,sMsg)  
        
    res = conn.getresponse()       
    body = res.read()  
    conn.close()  
    
    ddata=json.loads(body)
    errcode = ddata.get('errcode','')
    errmsg = ddata.get('errmsg','')
    return errcode,errmsg

def updateUser(sToken,sMsg):
    url = "/cgi-bin/user/update?access_token=%s"%(sToken)
    conn = httplib.HTTPSConnection('qyapi.weixin.qq.com')  
        
    conn.request('POST', '%s'%url,sMsg)  
        
    res = conn.getresponse()       
    body = res.read()  
    conn.close()  
        
    ddata=json.loads(body)
    errcode = ddata.get('errcode','')
    errmsg = ddata.get('errmsg','')
    return errcode,errmsg

def deleteUser(sToken,wx_id):
    url = "/cgi-bin/user/delete?access_token=%s&userid=%s"%(sToken,wx_id)
    conn = httplib.HTTPSConnection('qyapi.weixin.qq.com')  

    conn.request('GET', '%s'%url)  
    
    res = conn.getresponse()       
    body = res.read()  
    conn.close()  
        
    ddata=json.loads(body)
    errcode = ddata.get('errcode','')
    errmsg = ddata.get('errmsg','')
    return errcode,errmsg

def createDept(sToken,sMsg):
    url = "/cgi-bin/department/create?access_token=%s"%(sToken)
    conn = httplib.HTTPSConnection('qyapi.weixin.qq.com')  
        
    conn.request('POST', '%s'%url,sMsg)  
        
    res = conn.getresponse()       
    body = res.read()  
    conn.close()  
        
    ddata=json.loads(body)
    errcode = ddata.get('errcode','')
    errmsg = ddata.get('errmsg','')
    return errcode,errmsg

def updateDept(sToken,sMsg):
    url = "/cgi-bin/department/update?access_token=%s"%(sToken)
    conn = httplib.HTTPSConnection('qyapi.weixin.qq.com')  
    #print ToGBK(sMsg)
    conn.request('POST', '%s'%url,sMsg)  
        
    res = conn.getresponse()       
    body = res.read()  
    conn.close()  
    #print body
    ddata=json.loads(body)
    errcode = ddata.get('errcode','')
    errmsg = ddata.get('errmsg','')
    return errcode,errmsg

def deleteDept(sToken,dept_id):
    url = "/cgi-bin/department/delete?access_token=%s&id=%s"%(sToken,dept_id)
    conn = httplib.HTTPSConnection('qyapi.weixin.qq.com')  
    conn.request('GET', '%s'%url)  
    res = conn.getresponse()       
    body = res.read()  
    conn.close()  
        
    ddata=json.loads(body)
    print (body)
    errcode = ddata.get('errcode','')
    errmsg = ddata.get('errmsg','')
    return errcode,errmsg

def createTag(sToken,param):
    url = "https://qyapi.weixin.qq.com/cgi-bin/tag/create?access_token="+sToken
    res = requests.get(url,json=param)
    ddata = json.loads(res.content)
    errcode = ddata.get('errcode','')
    errmsg = ddata.get('errmsg','')
    return errcode,errmsg

mysql_config = {
    "host":'www.szoworld.cn',
    "charset":'utf8',   # or gb2312
    "database":'pram_sg',
    "user":'db_test',  
    "password":'qazedc'
}
dbs=pymysql.connect(**mysql_config)
db=dbs.cursor()
# db.execute(_sql)
# dbs.commit()
@Singleton
class WXQY:
    """ 企业微信api操作类 """
    source_url = 'https://qyapi.weixin.qq.com'      
    corp_id = None                                                                  # 企业id
    url_gettoken = source_url + '/cgi-bin/gettoken?corpid=%s&corpsecret=%s'
    address_book_corpsecret = None                                                  # 通讯录secret
    address_book_agentid    = None
    address_book_token = None                                                       # 通讯录操作token
    def __init__(self,corpid=''):
        self.corpid = corpid
    
    # 通过应用secret 获取token
    def gettoken(self,corp_secret,aid=''):
        if self.token:
            return self.token
        url = self.url_gettoken%(self.corpid,corp_secret)
        try:
            res = requests.get(url)
            if res.status_code is 200:
                res = json.loads(requests.get(url).content)
                if res['errcode'] is 0:
                    sql = "update wx_corp_agent set access_token='%s',expires_in='%s',token_utime=now() where id='%s'"%(res['access_token'],res['expires_in'],aid)
                    db.executesql(sql)
                    return res['access_token']
                return None
            else:
                return None
        except:
            # 网络连接错误
            return None

    # 获取数据库保存的token
    def read_access_token(self,aid):
        sql = """select ifnull(access_token,'') from `wx_corp_agent` 
                    where expires_in - time_to_sec(timediff(now(),token_utime))>30 and id='%s'"""%(aid)
        lT,iN = db.select(sql)
        if iN ==0 :
            token = ''  
        else:
            token = lT[0][0] 
        return token

    def up_wx(self,wx_id,usr_name,dept_id,sort,mobile,gender,email,enable,wx_status):
            sql = """select id,`corp_id`,`corpsecret`,`agentid` from `wx_corp_agent` where name='通讯录'"""
            lT,iN = db.select(sql)
            if iN ==0 :
                return [],[]
            aid = lT[0][0] 
            corp_id = lT[0][1] 
            corpsecret = lT[0][2] 
            agentid = lT[0][3]
            sToken =  self.read_access_token(aid) 
            if sToken == '':
                sToken = self.gettoken(corpsecret,aid)
            sMsg = """{
                    "userid": "%s",
                    "name": "%s",
                    "department": [%s],
                    "mobile": "%s","""%(wx_id,usr_name,dept_id,mobile)
            if gender == 0:
                sMsg += """
                    "gender": "2","""
            elif gender == 1:
                sMsg += """
                    "gender": "1","""
            sMsg += """
                    "email": "%s",
                    "enable": %s
                    }
                        """%(email,enable)
            #print ToGBK(sMsg)
            if wx_status == 1:
                return createUser(sToken,sMsg) 
            elif wx_status == 2:
                return updateUser(sToken,sMsg) 
            elif wx_status == 3:
                return deleteUser(sToken,wx_id) 
            return -1,'未知错误'

    # 初始化数据库中的企业微信通讯录信息
    def init(self):
        uL = []
        dL = []
        sql = """select id,`corp_id`,`corpsecret`,`agentid` from `wx_corp_agent` where name='通讯录'"""
        lT,iN = db.select(sql)
        if iN ==0 :
            return dL,uL
        
        aid = lT[0][0] 
        self.corp_id = lT[0][1] 
        self.address_book_corpsecret = lT[0][2] 
        self.address_book_agentid = lT[0][3] 
        sToken=  self.read_access_token(aid)
        if sToken == '':
            sToken = self.gettoken(self.address_book_corpsecret,aid)
        self.address_book_token = sToken
    
    # 企业微信部门列表
    @property
    def depts(self,dpet_id=1):
        url =self.source_url + "/cgi-bin/department/list?access_token=%s&id=%s"%(self.address_book_token,dpet_id)
        res = requests.get(url)
        if res.status_code is 200:
            body = res.content
            ddata=json.loads(body)
            deptlist = ddata['department'] 
            return deptlist
        else:
            print ('获取企业微信部门列表失败！')
            return []
    
    # 企业微信成员列表
    @property
    def users(self,dpet_id=1):
        url =self.source_url + "/cgi-bin/user/list?access_token=%s&department_id=%s&fetch_child=1&status=0"%(self.address_book_token,dpet_id)
        res = requests.get(url)
        if res.status_code is 200:
            body = res.content
            ddata=json.loads(body)
            userlist = ddata['userlist'] 
            return userlist
        else:
            print ('获取企业微信成员列表失败！')
            return []

    # 企业微信标签列表
    @property
    def tags(self):
        url =self.source_url + "cgi-bin/tag/list?access_token=%s"%(self.address_book_token)
        res = requests.get(url)
        if res.status_code is 200:
            body = res.content
            ddata=json.loads(body)
            taglist = ddata['taglist'] 
            return taglist
        else:
            print ('获取企业微信标签列表失败！')
            return []
        
    # 获取企业微信通讯录 标签、成员、部门 列表
    def get_address_book(self):
        pass

    def update_tag(self):
        tags = self.tags
        sql = """
            select role_id,role_name from roles 
        """
        rows,iN = db.select(sql)
        local_tags_id =  []
        local_tags =  {}
        if iN:
            for r in rows:
                local_tags_id.append(r[0])
                local_tags.update({'%s'%r[0]:r[1]})

        _tags_ids = []
        for _ in tags:
            _tags_ids.append(_.get('tagid'))
            _tags_name.append(_.get('tagname'))

        for i,local_id in enumerate(local_tags_id):
            if  local_id not in _tags_ids: # 更新
                param = {'tagname':local_tags_name[i],'tagid':local_id}
                createTag(self.address_book_token,param)
            else:
                if local_tags[local_id]!=local_tags_name[i]:
                        param = {'tagname':local_tags_name[i],'tagid':local_id}
                        createTag(self.address_book_token,param)



                

def getUsers(request):
    dL,uL = getInfoFromWx()
    
    #更新部门同步信息
    sql = """delete from synchro_dept_log where upd_status = 0 """
    db.executesql(sql)
    sql = """insert into `synchro_dept_log` (`dept_id`,`name`,`parentid`,`sort`,`upd_status`,`wx_status`)
             select id,cname,parent_id,sort,0,1 from dept where del_flag = 0
          """
    db.executesql(sql)
    sql = "select id,cname,parent_id,sort from dept where del_flag = 0"
    rows,iN = db.select(sql)
    L =[]
    sql = ''
    for e1 in rows:  #遍历本地部门
        dept_id1 = e1[0]
        name1 = e1[1]
        parentid1 = e1[2]
        order1 = e1[3]
        
        is_find = 0
        for e in dL:   #遍历企业号部门
            dept_id = e.get("id",'')
            name = e.get("name",'')
            parentid = e.get("parentid",'')
            order = e.get("order",'')
            if dept_id1 == dept_id:
                if name1!=name or str(parentid1)!=str(parentid):  #需要更新
                    sql += "update synchro_dept_log set wx_status=2 where dept_id=%s and upd_status=0;"%(dept_id)
                else:  #无需跟新
                    sql += "delete from synchro_dept_log where dept_id=%s and upd_status=0;"%(dept_id)
                is_find = 1
                break
    for e in dL:   #遍历企业号部门
        dept_id = e.get("id",'')
        name = e.get("name",'')
        parentid = e.get("parentid",'')
        order = e.get("order",'')
        is_find = 0
        for e1 in rows:  #遍历本地部门
            dept_id1 = e1[0]
            name1 = e1[1]
            parentid1 = e1[2]
            order1 = e1[3]
            if dept_id1 == dept_id: 
                is_find = 1
                break
        # 增加更新部门记录（wx_status=3 delete upd_status=0 ）  
        if is_find == 0:
            sql += """insert into `synchro_dept_log` (`dept_id`,`name`,`parentid`,`sort`,`upd_status`,`wx_status`) 
                       values (%s,'%s',%s,%s,0,3);
                  """%(dept_id,name,parentid,order)    
    #print sql
    db.executesql(sql)

    #更新人员同步信息
    sql = """delete from synchro_user_log where upd_status = 0 """
    db.executesql(sql)
    # 当用户没有被禁用时 u.status = 1   ##。。。。
    sql = """insert into `synchro_user_log` (`usr_id`,wx_id,`usr_name`,`dept_id`,`sort`,`mobile`,`gender`,`email`,`enable`,`upd_status`,`wx_status`)
             select u.usr_id,ifnull(wxqy_id,login_id),u.usr_name,u.dept_id,u.sort,ifnull(a.mobile ,u.`mobil`),a.sex,ifnull(a.email,u.e_mail),u.status,0,1 from users u 
                left join empl e on e.usr_id = u.usr_id
                left join `addr_book` a on a.emp_id = e.id                                                                  
                where u.status = 1
                order by u.usr_id
          """
    
    db.executesql(sql)
    sql = """select ifnull(wxqy_id,login_id),u.usr_name,u.dept_id,u.sort,ifnull(a.mobile ,u.`mobil`),ifnull(a.sex,''),ifnull(a.email,u.e_mail),u.status,u.usr_id from users u 
                left join empl e on e.usr_id = u.usr_id
                left join `addr_book` a on a.emp_id = e.id                                                                  
                where u.status = 1
                order by u.usr_id"""
    rows,iN = db.select(sql)
    L =[]
    sql = ''
    for e1 in rows:  #遍历本地人员
        usr_id1 = e1[0]
        name1 = e1[1]
        dept_id1 = e1[2]
        order1 = e1[3]
        mobile1 = e1[4]
        gender1 = e1[5]
        email1 = e1[6]
        enable1 = e1[7]
        
        is_find = 0
        for e in uL:   #遍历企业号人员
            usr_id = e.get("userid",'')
            name = e.get("name",'')
            dept_id = e.get("department",'')
            dept_id = dept_id[0]
            order = e.get("order",'')
            order = order[0]
            mobile = e.get("mobile",'')
            gender = e.get("gender",'')
            email = e.get("email",'')
            enable = e.get("enable",'')
            if usr_id1 == usr_id:
                #手机号只能自己更新  
                if name1==name and dept_id1==dept_id and email1==email and enable1==enable:  #无需跟新
                    sql = "delete from synchro_user_log where wx_id='%s' and upd_status=0;"%(usr_id)
                    #print sql
                    db.executesql(sql)
                else:  #需要更新
                    print "%s %s %s %s %s "%(usr_id,dept_id,mobile,email,enable)
                    print "%s %s %s %s %s "%(usr_id1,dept_id1,mobile1,email1,enable1)
                    sql = "update synchro_user_log set wx_status=2 where wx_id='%s' and upd_status=0;"%(usr_id)
                    #print sql
                    db.executesql(sql)
                is_find = 1
                break
    for e in uL:   #遍历企业号人员
        usr_id = e.get("userid",'')
        name = e.get("name",'')
        dept_id = e.get("department",'')
        order = e.get("order",'')
        mobile = e.get("mobile",'')
        gender = e.get("gender",'')
        email = e.get("email",'')
        enable = e.get("enable",'')
        status = e.get("status",'')
        is_find = 0
        for e1 in rows:  #遍历本地人员
            usr_id1 = e1[0]
            name1 = e1[1]
            if usr_id1 == usr_id: 
                is_find = 1
                id = e1[8]
                sql1 = "update users set wx_status = %s where usr_id=%s"%(status,id)
                db.executesql(sql1)
                break
            elif name == name1 and mobile==e1[4]:
                is_find = 1
                id = e1[8]
                sql1 = "update users set wxqy_id = '%s' where usr_id=%s"%(usr_id,id)
                db.executesql(sql1)
                break

        if is_find == 0:
            sql = """insert into `synchro_user_log` (wx_id,usr_name,`upd_status`,`wx_status`)
                       values ('%s','%s',0,3);
                  """%(usr_id,name)    
            db.executesql(sql)
  
    sql = "select `dept_id`,`name`,`parentid`,wx_status from synchro_dept_log where upd_status=0" 
    rows,iN = db.select(sql)
    names = 'id cname parent_id wx_status'.split()
    L = [dict(zip(names, d)) for d in rows]
    deptData = json.dumps(L,ensure_ascii=False)      

    sql = "select usr_id,usr_name,dept_id,wx_status from synchro_user_log where upd_status = 0"
    rows,iN = db.select(sql)
    names = 'usr_id usr_name dept_id wx_status'.split()
    L = [dict(zip(names, d)) for d in rows]
    userData = json.dumps(L,ensure_ascii=False)      

    s = """
        {
        "errcode": 0,
        "errmsg": "获取用户列表成功",
        "deptList":%s,
        "userList":%s
        }
        """%(deptData,userData)
    #print s
    return HttpResponseCORS(request,s)      









def main():
    files = {'media':open("S:/GitHub/design_mode/qywx/batch_user_samples.csv", 'rb')}
    url = 'https://qyapi.weixin.qq.com/cgi-bin/media/upload?access_token='+token+'&type=file'
    # token = 'TA3u-J6g43G5_OSTrko7EAtZ6RyCL7_rDp09Nd89u6PkU_ocDh6sMB92PDGL1KhNzhZq3T6yYaYp-xgV4UCIHXa2cIoK7fL4YAn72DsQVpL3gX4xuv3lLtQspqN2sKSAM6MLq0encCZnkVW3kt67OSZVjnzMUfcKuBxibuEy_sI5bSfJa818n9jKFfkAjCQNCs75WNegIYIC70P3S2TaDA'
    param = {'access_token':'TA3u-J6g43G5_OSTrko7EAtZ6RyCL7_rDp09Nd89u6PkU_ocDh6sMB92PDGL1KhNzhZq3T6yYaYp-xgV4UCIHXa2cIoK7fL4YAn72DsQVpL3gX4xuv3lLtQspqN2sKSAM6MLq0encCZnkVW3kt67OSZVjnzMUfcKuBxibuEy_sI5bSfJa818n9jKFfkAjCQNCs75WNegIYIC70P3S2TaDA'
            ,'type':'file'}
    res = requests.post(url,{'type':'file'},files=files)
    _res = json.loads(res.content)
    # print(_res)
    # media_id = '3NGOiuIvSLOc3AVYmd1J7RTB2l5MuP8lq9UcoLTCKhFQ'
    media_id = _res['media_id']
    url = 'https://qyapi.weixin.qq.com/cgi-bin/batch/syncuser?access_token='+token+'&media_id='+media_id
    print(url)
    res = requests.post(url,json={'media_id':media_id,'to_invite':False})
    print(res.content)
    print (res)
    url = 'https://qyapi.weixin.qq.com/cgi-bin/media/get?access_token='+token+'&media_id='+media_id
    r = requests.get(url, stream=True)
    with open("test1.csv", "wb") as code:
         code.write(r.content)
    
if __name__ == "__main__":
    corpid = 'wxbe2dd354f1b37b11'
    secret = '0E-5z9z7j8svA2BxMG-fqAMPiPCd_BI0Yw3VNg5BL_g'
    wx = WXQY(corpid)
    # token = wx.gettoken(secret)
    # print(token)
    token = 'TA3u-J6g43G5_OSTrko7EAtZ6RyCL7_rDp09Nd89u6PkU_ocDh6sMB92PDGL1KhNzhZq3T6yYaYp-xgV4UCIHXa2cIoK7fL4YAn72DsQVpL3gX4xuv3lLtQspqN2sKSAM6MLq0encCZnkVW3kt67OSZVjnzMUfcKuBxibuEy_sI5bSfJa818n9jKFfkAjCQNCs75WNegIYIC70P3S2TaDA'
    param = {
    "userid": "zhangsan",
    "name": "Micheal",
    "alias": "jackzhang",
    "mobile": "15913215421",
    "department": [2],
    "position": "产品经理",
    "gender": "1",
    "email": "zhangsan@gzdev.com",
    "is_leader_in_dept": [0],
    "enable":1,
    "telephone": "020-123456",
    "address": "广州市海珠区新港中路"
    }
    url = 'https://qyapi.weixin.qq.com/cgi-bin/user/create?access_token='+token
    res = requests.post(url,json=param)
    print(res.content)
    # main()
    
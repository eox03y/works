소스가 있는 곳의 디렉토리 밖에서 appcfg.py를 실행한다. 소스 디렉토리 이름을 알려주어야 한다.

$ ./google_appengine/appcfg.py  update   jeenee-kr/
$ ./google_appengine/appcfg.py --email=handol@gmail.com update jeenee-kr/


# https://bitbucket.org/mchaput/stemming
# porter stemmer 2

$  ./google_appengine/appcfg.py --email=handol@gmail.com backends jeenee-kr/ update worker
# http://jeenee-kr.appspot.com/_ah/start 를 브라우져에서 호출
# http://worker.jeenee-kr.appspot.com/

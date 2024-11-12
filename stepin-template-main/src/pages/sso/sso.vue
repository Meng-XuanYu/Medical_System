<html>
<head>
<title>统一身份认证</title>
<meta charset="UTF-8"><meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1"><meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no"><meta name="renderer" content="webkit"><link rel="stylesheet" href="/css/bootstrap.min.css"><link rel="stylesheet" href="/css/index.css"><!--[if lt IE 9]>
<script src="/js/respond.min.js"></script>
<![endif]--><script src="/js/jquery.min.js"></script>
<script src="/js/bootstrap.min.js"></script>
</head>
<body>
<iframe id="loginIframe" src="/cas/login-normal.html"></iframe>
<div id="default" class="container" style="display: none;">
  <div class="border col-lg-4 col-lg-offset-4 col-md-4 col-md-offset-4 col-sm-6 col-sm-offset-3">
    <div class="system">统一身份认证</div>
    <div class="service" id="targetSystem">WebVPN系统</div>
    <div class="service" id="targetSystemDescription" style="display: none;"></div>
    <form method="post" id="loginForm" action="login">
      <div class="form-group">
        <label>
          <span>用户名</span>
          <input type="text" class="form-control" name="username"></label>
      </div>
      <div class="form-group">
        <label>
          <span>密码</span>
          <input type="password" class="form-control" name="password" autocomplete="off"></label>
      </div>
      <div class="form-group" style="display: none;" id="captchaParent">
        <label>
          <span style="display: none;" id="captchaLabel">验证码</span>
          <div id="captchaDiv"></div>
        </label>
      </div>
      <div class="form-group">
        <input class="btn btn-login" type="submit" name="submit" value="登录"></div>

      <div style="display: none;">
        <input name="type" value="username_password"><input name="execution" value="8e89c9eb-ab21-4d54-9b21-6ac85e10103c_ZXlKaGJHY2lPaUpJVXpVeE1pSjkuUnVMMkdGeHk1bFpLL0o3NWNvcnRDczZ1RHMzTWhYV1JiOGh3a1ZRV1diYkppMWE2NTBsVTJxdmlYTURwZk90bUk0Uk5VQjZYNnVhNS9HYlNkcFBONnNUM2JzQ3pEeWIrTUxTa09Hdm85V0hqd3BGN05oTDh0RXV6QlU3WG9pWWVwM2E0Z0Z0OVVlVFhVMmRmbXo0ejFteCtNNUUrNGsrOC93VmYvbnM0Z3NCQWRpWklTTTBvb1FBVHFEWm0rSjNNeFpkTkFTZkgySjhhUjBtTVRkZStIVDdKNVRxdjhENmlaQjVYR2J5ckJHNmFVS3NvVGdldlBTRyt2cHF2NFZYMTQ3Q0pydzZxRUIzY0xOcVB4cndwc2orT0szTEg2REhxUTlteXc3K0NwNExPTDlSRlJSMGR1VXNtc08zRUZWbUZ5VVg3WVVjVTF3c1dmSTVHeVNPWFoxNTNDWDBrWXROZXJycDhPb3JlYTBZQkhEUmYrWW44QlJVNS9Ja2NJc2x3MlMvYXFaeXo5bm42RmM2cHZxZFRSSHJFMEZxRXdUbE1TUGV2bkQ0TW5POE8wUm5QQ1hNcmVEcUgrZ0VwdysxS1F6Wm5zN2JWSEpSa2F1NnVqRDdERzVWeEhzWjlkK0tCbUo2R3N5RGN6YUExTS9Na1Nrd3FYYThsYklZNDFkcWFFVFlINUFINTY3b0JCbTA0bnA3V3Q5OUpoU3RBTExTbGhsN1NhTlR4aVUrMlFFUXFIdnhHNDZCTU4rY050c1MvaGJwY0crZE5jVGVLNG9vaDhJL1BSTlZBcHhjUUUrOExSZ29VSEpUNjNDZnlyd3BEUTZmdHNoNkZIcVZUVGljSnJHaCsrRUlsUWJKaEUyM1prQjVGcVhUa2ZXWFJPRkJLYThKendkNFV0NnJOd1VSeGU1U3k5QjNBTlEyVHhUSUFUeGVWM1pGZW5QRGRKYmgyL01XVWhGSGM1aXdlbXk4c0FkZFdIL0ZXSWZqTU1IYUw5a1VUZGR3NGwxTjVDWWpFamJQSjMrTmtaMCt3ZWV2M3I0dWNvVkY3LzRvdmhOYXBjQVM5eklaU2h5a2JWTDFObE9oMUVvNEpVZ09QWWI1cUk4Rk5CNlUwSkZudUNTeUdtZ2hGS0FBODZJUEk4cnI2SHlVT280VTBnYUxMYWQ0SEJHSUlVWS9GN0IwclJDZUZkaUNCQml6RVY4dmZKNG95NHdJa213YWZFWDA0OHVwNU12RlhXU1ZMbVZ4a0lYNVBvYkJYNVplMTMzMG0wYVRjUG5VRUd6MCtRWld5bks5VWZwWnVNdkV1RjVOSGJGUTl0dFpCN0VobVo3amNyLzI0anVGMHNPRjFKd0plbTEzeXI0UExUK1hGVDBxZXZDRFFYYlhTRm5UamsrR1ZVS0w1cll4M0Y0WVM5NVpvRzhOOG54eXcxZlpNMzZLNWErRndpWFBLTWhzaHE5cTZpN0tIVFBsbVJDSmliNmJsdk1hWllLSy9RdFM2Skx1eEt6eVhhQUhjOG9KOExESFlUUFpjNVU5TGV6bFZ4V05sRi91alJ0NzVJbktVLzJLTnJHKzNGR0JFbEFWdjgvbzJlL3BnT00yTThLYzdSNC94VUU1R2M3WmtCL2xkSkoxWkxUQ2p4RENMaEoyOEVoVllWOVVHakVtSk0yWXphVUZJdVJUWXNUU3djU2dSNEJHam5sK1MrWTBSR0Z3OXZERmI4K05zS2pVTzZOK2tsMEZpNlJ6U21ZQ1hFMG1uVXZHRms2VjZOTGpsdXpoVzAwUzlNc2hhYXBRS1FVdEZLZmpZL1RPenZnWng3RlpydG82cjJPd3Q4dVhIdUV3Y2Zsdmh0RWhldWpqSFIyL0RtMUxlZWl3Q1JxOXZQS3hJVVJFeElJUnFQVDBGRDNFZWJOZitwb1FWR2pFeUpYYXRDK25WR1RUN2hjRVAwUnpoejQxNldKb0JHakRvSHJ5U1B4NUdxNzdLa0gxZW5Hd2t5VytaNXJnTDhFVFFBRkJ2MWNRc2NZMUc1ZmcyM1RyZjU1L2NtSEdvV0cwdVh3Qzg1SGJMeXRvdHFWTWNoM1lUNWR5a013dUYxekc3b3JiczdjckVTN0NlZ3licG5MUnBTUU8rSmpPV0Y0UXN3cjhvU2x1R0pvbVZtS1ArdS85MXppc1ZGYzFoR2tKOXZXSTlXcWNjVU05OVZWdXgwNWpYZHRsS2lBN3hFa3MvVGZCWjVuTFp0cW51T2wrQXRiNUlIdmVCTEtJV0dPSHhyTksyWjlTL1JrMUdLZ29UcC9zMXh3bEUwRVdLRHl2aGRqcldSd29CSjdjNmNoQmlwQmtkYkh1ZFBlMnhFU2NQWVdYZ2hDWlordVE4Q3ZJeTA3OGxxdlVsZUtNZ2ozM1BhMldnb01MR2FvMVpFNmUxdnpnYWxCRVlWQjYrcmtvQ2JSQ0F4VGVaVk00QkVxVDRhWDFCcmlyUGpMZmEweGNjQUEyejR6SnpETXJKbWtOcUMvT3ozRWlYTkQ4UEM3a2JycGxFSExrN1NvMkpHeHFvMlArU3EvWDZiOWh4M3BJRlpzSlorTnpMcXJwSTJtM1RGanZ5SzA3WERXZFZqY2ZSY3JqRTVFTE1sZmx1MEdML1h2VzBJSllkazJlRUQ3a0ExWEg2Sm1iUVZFaFlEUnZvaFdLY2UvVFF4RWVqbnI3VUtqWDFlcWFYdXI4Mm9BQi9nRmsvTlF4dXo3OG95MEM5MmtGSnR4ck1Ga2V3T3U0V2R2bzg3LzEyejZFb3VvbnAxOStGM0JvaTVjOG41a2ducjM3cU1rWUJQZCtBSk50M25pNDRzck9OeDdVNU1WWnFVeHQyY2FIYWY5dGEvbHZ1bXBndnZXSkdLSVgvVVROUEFOdGQ0dFB0amg2a1V4MnZxWmRSZ0luQTJIU1FvRmxmOXpEbUpIVjA1WkhoZVk1NHdURDNtQnVKUEdsWndvbnNFeGREVm1mai9uNXBVY1A0MllZTThqdVZhREZGVGZDUVhZM3RxV1Z3dG9uYnVRVm01UzJkZVVJd2pyZXYvZHpBM25TSG9wQXcvbFRNa3lHZXFPN2ZWaFY1UU81SVVpc2gyVmhyVmdISndnbDBsZmtXNmtlaW1zd04xaW5MUDBOWXkxZUFQNVl5dW8wRlFuVU9mS2VnZTFpMmpiT0hZbElVUGdYYWVma2tjSWhnRnU4K0dOVUFEZEtQbU1aRit5czVHditMVDNYaFhQT1laQkFETlBpNG0yUW1EcVgrNEMrRHA5RDJjRkMxVjJtekZnT0hhSlM4aDlmVVlnSnFPd2d5YldlY29QNk1sa1lJa2hzczlpc0p2a3J3OThDQktnbnRiUlpRRjdOV2Z4M29HZVkzeHh3dzBRMk9hYUIwUmNjRklZRHBwNUtQRHVWaWxXbTl2U1ZhYVY4bjhXNW53ZEZKcVJZRTJCamZsdXY2WXVVRnRIVDdxZTNRVWxUemRmeTh3cnRUbHZ0OFJjemRpWEJ0SnFManlCU1JxWXdEamNaK25RSEw0U1pMeXAweTlxSmNGYUJSUldSdUFBeFpTM29paFZ4TzFXK1lvQnVSelBzNDhsQW9mR1dPajhiZTdKMVp6QWVPb1JqbStsYXQ3NGwzczlhZXJjSDBreCt2WlkxVzlvKzNKVW1KMU1GUW5yYVgyckN6QUFvdUp0ODU4N3VRZXVVV1RmbC9DaGN2ZDZyL0VGbnNSZkY0c00zTkdmeWJ1cWhmNlJyL3YvMHplV0oyTUI2T0dROXdVY3ZCZWFnUGowRUtOVFNqVHBXSEhFbHJHUFRUS2c0U01iYk8wdjUzNlNCSHFFMm9zdlBoakNVY1QzWm1tdE55OFh6QWwvR0tKRnlqNnZYRTlZNFFKSXNablBob0ZwcVFreStsSG81K3pNdWlpWEZnR0cxN251czdVcVVxMm1RRmcvTWxxYjhwZmRuaXVUM1M3ZHk0RHdIMDgvN2U1R0paQW9rRWdGeG5qSjBOcHZYZmlFNlhNamZlcXd5M05tZnJjNSsybDhtb2puTDIxWDNQQXIvdlRyNUN6Y3hEdzlRKy9HajFXUmVjOVpSanlXbEpLVmVBckM4MFdrNWpWNGFEOC9CMlBUWDBHbllTWXQ4d2ZiS01CWHZHVHJUZmxRR1ZVNTJRQ1pjaTVBb2hDSThWOWZsVjAxU1JLRU9jbHc0a2hmdlRwVm1ETWQ3a29jekt0empiUVk5ZE1acDRBUHdzbW5uSEdLR0JMb2VqMXJHRHo1Tm5LZE1ENFRoVDM4NS8vK01nMURPVXhnc05zbHhrNjlzTEJwQlRpdC91UnozQ2NUMENhdmdHY0FpNWJpVngySTBtcmxKQzFrLzNDNlg5QitsWlFlNlZSd0lKTnFqQkdBTEpSMTYwcVQ0c1lhMjNFRUljTnY4UzQrZk1QcitZTVkwdGh0alVkYmlBZGxNNFRJSStoTzdUVHFxRXBPMTNUT3hQRWdMMnJ3VklBVGxieHpqOUFXVDlZbDFPSWp2bGdqMzFRVGZuTWVZa3A4L3VjdTViTXBlMUtJUm9vNXRSbUZ0cDJOMW1MMFZQbkd6V3RKTk01ak52Mmp1YlpZRTQrS01oV25vaVBHaHl2UnR6UDYvMm9BTHJ5bUFQMGRwV1piQWEwLzZSVTZ0NTBwUmQ2L0dXeUFjbkpQbEdvcHkrL3BlZlYrZ09NbW4wMy94ak1lRG9adTRHYktWaHBsVzlScHlGc2FpbzdaZTl2UUxpVGJGNHFMWGhiWm56ZS9iREtTZ2ZrdVNxUXM2Nm50N1piU3lqcCs4akx6YTc1S0ZXM0tGRXFMb3V1UVNFeGk4RXVkNXNjL3FBcll6eG9FdmFyMHpkYS82c25MT0RwWFg2L2RSVlJESU1kVUtuM1VGSkVGbURWMFQwdHl2c0RMZzkzVVpZejNXWTVwekFDekJjS1l0OWRhR2ZaYzl0UVdRQ0UzaS92QnA3bi95djZUeHZ0ZXZXV28raHJkeTR1L1FOUGNDU2RRUW5SWUxrVHQzODlqOEQ0dE9tNnBrbzBLeUNpUHh0Q0FnUC9jZmYvRml5YXVCQW1vd2c5SHBiMlB1d0xoQnNiVHBjeWhxRFRiNzloTGVhdnZic2pOaTNGRjZmNmlmL1BlemZ2MzcxRjlaNk4wL2dBZS91cGxjUkg0TDVVazdEVmd1c1d4LzNqZHczR1d3Y3IxZzFXQTdYVmtNd1F1elZqeEs5bnRuQ1FSUU9obTFmY3I4OFlPMzFGWDRNR3NNREQ2QnJCVU1OY0V6ZWNZM1RWR212L0FmSVdEdllPQ1VCZ0tLVTlnTjZZUUg3RnUvNm9FTVMzZkxDNGhrcG1rb2lxODhLQS9kQ1QrMWliL1NvMFdJTzMrZ01Qekp2TURYN0g1Qndxdz09Lmw1SndjOEI4Nzc5eEhQN1pYQUV1eG1hSFFvYzB2TUtQVTFuaXNPQllGZDFGOTlVWmVGeUNWdVFwUTVDU2pDNkxZUXJtbkpyeThLMmFEaW9DZEw3VUx3"><input name="_eventId" value="submit"></div>
    </form>
    <div class="hint">此页面为兼容性视图<br>请使用Chrome等现代浏览器以获取最佳体验</div>
  </div>
</div>
<div id="language" style="display: none">zh_cn</div>
<div id="pac4jUrls" style="display: none">
  <a href="clientredirect?client_name=cas&amp;service=https://e1-443.e1.buaa.edu.cn/users/auth/cas/callback?url%3Dhttps%253A%252F%252Fe.buaa.edu.cn%252F">cas</a><a href="clientredirect?client_name=mc-qr&amp;service=https://e1-443.e1.buaa.edu.cn/users/auth/cas/callback?url%3Dhttps%253A%252F%252Fe.buaa.edu.cn%252F">mc-qr</a><a href="clientredirect?client_name=mc-wx&amp;service=https://e1-443.e1.buaa.edu.cn/users/auth/cas/callback?url%3Dhttps%253A%252F%252Fe.buaa.edu.cn%252F">mc-wx</a>
</div>
<script type="text/javascript">
  function getParameterByName(name, url) {
    if (!url) url = window.location.href;
    name = name.replace(/[\[\]]/g, '\\$&');
    var regex = new RegExp('[?&]' + name + '(=([^&#]*)|&|#|$)'),
      results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, ' '));
  }

  var config = {};
  // 当前语言
  config.locale = $("#language").text();
  // 错误信息
  config.error = $("#errorDiv p").text() || null;
  // 登录目标系统
  var targetServiceName = $("#targetSystem").text() || null;
  var targetServiceDescription = $("#targetSystemDescription").html() || null;
  if (targetServiceName) {
    config.service = {
      name: targetServiceName,
      description: targetServiceDescription,
      href: getParameterByName('service') || getParameterByName('target') || getParameterByName('TARGET')
    };
  }
  // 第三方授权登录链接
  var pac4jAs = $("#pac4jUrls a");
  if (pac4jAs.length > 0) {
    config.pac4j = [];
    pac4jAs.each(function(i) {
      config.pac4j.push({
        href: pac4jAs[i].href,
        name: pac4jAs[i].innerText
      });
    });
  }

  function getPageConfig() {
    return config;
  }

  var firstLogin = true;
  function doLogin(username, password, type, captcha) {
    if (firstLogin) firstLogin = false;
    else return;

    var lginfm = document.getElementById('loginForm');
    $("#loginForm input[name='username']").val(username);
    $("#loginForm input[name='password']").val(password);
    $("#loginForm input[name='type']").val(type);
    if (captcha) {
      $("#loginForm input[name='captcha']").val(captcha);
    }
    $("#loginForm input[name='submit']").click();
  }

  function setLanguage(locale) {
    var fullURL = window.location.href;
    if (fullURL.indexOf('locale=zh_cn') !== -1) {
      window.open(fullURL.replace('locale=zh_cn', 'locale=' + locale), '_self');
      return;
    }
    if (fullURL.indexOf('locale=en') !== -1) {
      window.open(fullURL.replace('locale=en', 'locale=' + locale), '_self');
      return;
    }
    var baseURL = fullURL.split('?')[0];
    var params = window.location.search.substring(1);
    if (params.length > 0) params = '&' + params;
    window.open(baseURL + '?locale=' + locale + params, '_self');
  }

  function ie8() {
    return navigator.appName === "Microsoft Internet Explorer"
      && parseInt(navigator.appVersion.split(";")[1].replace(/[ ]/g, "").replace("MSIE", "")) <= 8;
  }
</script>
<script type="text/javascript">
  config.mobileCampus = {
    baseHost: 'app.buaa.edu.cn',
    security: true,
    baseUrl: 'https://app-443.e1.buaa.edu.cn',
    appid: '200190528091014504',
    title: '信息北航',
    autoRedirect: false
  };
</script>
<script type="text/javascript" src="/cas/js/init.js"></script>

</body>
</html>
<script setup lang="ts">
</script>
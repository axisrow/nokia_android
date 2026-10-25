package retro.nokia;
import android.app.Activity;
import android.os.Bundle;
import android.webkit.WebView;
import android.webkit.WebChromeClient;
import android.webkit.ConsoleMessage;
import android.webkit.WebResourceError;
import android.util.Log;
import android.webkit.WebViewClient;
import android.webkit.WebResourceRequest;
import android.webkit.WebResourceResponse;
import java.io.ByteArrayInputStream;
import android.graphics.Color;
public class MainActivity extends Activity {
 private WebView web;
 @Override public void onCreate(Bundle state) {
  super.onCreate(state);
  getWindow().setStatusBarColor(Color.rgb(17,25,30));
  getWindow().setNavigationBarColor(Color.rgb(17,25,30));
  if ((getApplicationInfo().flags & 2) != 0) WebView.setWebContentsDebuggingEnabled(true);
  web=new WebView(this); web.setBackgroundColor(Color.rgb(17,25,30));
  web.getSettings().setJavaScriptEnabled(true);
  web.getSettings().setDomStorageEnabled(true);
  web.getSettings().setAllowFileAccess(false);
  web.getSettings().setAllowContentAccess(false);
  web.setOnApplyWindowInsetsListener((view, insets) -> {view.setPadding(insets.getSystemWindowInsetLeft(),insets.getSystemWindowInsetTop(),insets.getSystemWindowInsetRight(),insets.getSystemWindowInsetBottom());return insets;});
  web.setWebChromeClient(new WebChromeClient(){
   @Override public boolean onConsoleMessage(ConsoleMessage msg){if(msg.messageLevel()==ConsoleMessage.MessageLevel.ERROR)Log.e("NokiaWebView",msg.message());return true;}
  });
  web.setWebViewClient(new WebViewClient(){
   @Override public void onPageFinished(WebView v,String url){Log.i("NokiaWebView","Page loaded: "+url);}
   @Override public void onReceivedError(WebView v, WebResourceRequest req, WebResourceError error){Log.e("NokiaWebView","Load error "+error.getErrorCode()+": "+error.getDescription());}
   @Override public WebResourceResponse shouldInterceptRequest(WebView view, WebResourceRequest req){
    String url=req.getUrl().toString();
    if(url.startsWith("https://retro.local/")){
     String path=req.getUrl().getPath().substring(1);
     String mime=path.endsWith(".js")?"application/javascript":path.endsWith(".css")?"text/css":path.endsWith(".wav")?"audio/wav":"text/html";
     try{return new WebResourceResponse(mime,path.endsWith(".wav")?null:"UTF-8",getAssets().open(path));}catch(Exception e){}
    }
    return new WebResourceResponse("text/plain","UTF-8",new ByteArrayInputStream(new byte[0]));
   }
   @Override public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest req){return !req.getUrl().toString().startsWith("https://retro.local/");}
  });
  setContentView(web); web.loadUrl("https://retro.local/index.html");
 }
 @Override protected void onPause(){super.onPause();web.onPause();web.evaluateJavascript("if(typeof audio!=='undefined')audio.pause()",null);}
 @Override protected void onResume(){super.onResume();if(web!=null)web.onResume();}
 @Override public void onBackPressed(){web.evaluateJavascript("menu()",null);}
}

import com.badlogic.gdx.files.FileHandle;
import com.badlogic.gdx.graphics.g2d.TextureAtlas.TextureAtlasData;
import com.badlogic.gdx.utils.Json;
import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;
import java.util.HashMap;
public class ReligionIconDiagnostic {
 public static void main(String[]a)throws Exception{
  var d=new TextureAtlasData(new FileHandle(a[0]+"/game.atlas"),new FileHandle(a[0]),false);
  var pages=new HashMap<String,BufferedImage>();for(var p:d.getPages())pages.put(p.textureFile.path(),ImageIO.read(p.textureFile.file()));
  String[] names=new Json().fromJson(String[].class,new FileHandle(a[0]+"/jsons/Religions.json"));
  for(String name:names){
   boolean ok=false;
   for(var r:d.getRegions())if(r.name.equals("ReligionIcons/"+name)){
    var img=pages.get(r.page.textureFile.path());if(img==null||r.left<0||r.top<0||r.left+r.width>img.getWidth()||r.top+r.height>img.getHeight())throw new AssertionError("Invalid region "+name);
    int opaque=0;for(int y=r.top;y<r.top+r.height;y++)for(int x=r.left;x<r.left+r.width;x++)if((img.getRGB(x,y)>>>24)!=0)opaque++;
    if(opaque==0)throw new AssertionError("Blank icon "+name);ok=true;
   }
   if(!ok)throw new AssertionError("Missing icon "+name);
  }
  System.out.println("Native atlas: "+d.getPages().size+" pages, "+d.getRegions().size+" regions; "+names.length+" religion icons present, bounded and nonblank. No game created.");
 }
}

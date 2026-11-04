import com.badlogic.gdx.Gdx;
import com.badlogic.gdx.backends.lwjgl3.Lwjgl3Files;
import com.badlogic.gdx.files.FileHandle;
import com.unciv.models.ruleset.*;
import com.unciv.models.ruleset.validation.*;
public class NativeRulesetValidation {
 public static void main(String[]a){
  Gdx.files=new Lwjgl3Files();
  RulesetCache.INSTANCE.loadRulesets(true,true);
  var r=new Ruleset();r.setFolderLocation(new FileHandle(a[0]));r.load(new FileHandle(a[0]+"/jsons"));
  var nativeAssets=new Ruleset();nativeAssets.setName("Native asset lookup");nativeAssets.setFolderLocation(new FileHandle(a[1]));
  RulesetCache.INSTANCE.put("Native asset lookup",nativeAssets);RulesetCache.INSTANCE.put("FantasyUnciv",r);
  r.getMods().add("Native asset lookup");r.getMods().add("FantasyUnciv");
  var errors=RulesetValidator.Companion.create(r,true).getErrorList();System.out.println(errors.getErrorText(true));
  for(var e:errors)if(e.getErrorSeverityToReport()!=RulesetErrorSeverity.OK)System.exit(1);
  System.out.println("Native ruleset validation passed with builtin and MOD asset lookup. No game or GL context created.");System.exit(0);
 }
}

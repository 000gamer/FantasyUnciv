import com.unciv.models.ruleset.Ruleset;
import com.badlogic.gdx.files.FileHandle;
public class HeroFilterDiagnostic {
 public static void main(String[] args) {
  var rs=new Ruleset();rs.load(new FileHandle(args[0]+"/jsons"));
  String[] roles={"英雄近战","英雄施法","英雄近战","英雄生物","英雄施法","英雄幽魂","英雄施法","英雄施法","英雄海军","英雄近战","英雄近战","英雄近战"};
  int count=0;
  for(int i=1;i<=12;i++){
   String id=String.format("H%02d",i);var u=rs.getUnits().get(id);u.setRuleset(rs);
   if(!u.matchesFilter(roles[i-1],null,true))throw new AssertionError(id+" lost original role filter");
   if(!u.matchesFilter("Hero",null,true))throw new AssertionError(id+" lost hero exploration filter");
   if(u.matchesFilter("P71",null,true)!=(i>=5))throw new AssertionError(id+" visitor cap tag differs");
   count+=3;
  }
  for(var u:rs.getUnits().values())if(!u.getName().matches("H[0-9]{2}")){
   u.setRuleset(rs);if(u.matchesFilter("Hero",null,true)||u.matchesFilter("P71",null,true))throw new AssertionError("ordinary unit matches hero tag "+u.getName());count++;
  }
  System.out.println("Native base-unit filter assertions passed: "+count+". No game, map, or turn created.");
 }
}

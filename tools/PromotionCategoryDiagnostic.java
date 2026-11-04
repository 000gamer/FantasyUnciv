import com.unciv.models.ruleset.Ruleset;
import com.badlogic.gdx.files.FileHandle;
public class PromotionCategoryDiagnostic {
 public static void main(String[] args) {
  var r=new Ruleset();r.load(new FileHandle(args[0]+"/jsons"));
  for(String[] pair:new String[][]{{"P41","Hero-01"},{"P42","Hero-01"},{"P110","Hero-03"},{"P111","Hero-03"}}){
   var p=r.getUnitPromotions().get(pair[0]);var category=p.getSubCategory(r);
   if(!pair[1].equals(category))throw new AssertionError(pair[0]+" wrong category "+category);
   System.out.println(pair[0]+" -> "+category);
  }
  System.out.println("Native Civilopedia category assertions passed. No game, map or UI created.");
 }
}

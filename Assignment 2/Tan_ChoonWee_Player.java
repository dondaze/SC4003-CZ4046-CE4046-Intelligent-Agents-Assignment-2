class Tan_ChoonWee_Player extends Player {
   int selectAction(int n, int[] myHistory, int[] oppHistory1, int[] oppHistory2) {
      // Rule 1: Be nice - Start by cooperating
      if (n == 0) return 0;

      // Rule 2: Retaliate appropriately — punish immediately if any opponent defected last round
      if (oppHistory1[n - 1] == 1 || oppHistory2[n - 1] == 1) {
         return 1;
      }

      // Calculate defection rates for both opponents
      int defectCount1 = 0, defectCount2 = 0;
      for (int i = 0; i < n; i++) {
         defectCount1 += oppHistory1[i];
         defectCount2 += oppHistory2[i];
      }
      double defectRate1 = (double) defectCount1 / n;
      double defectRate2 = (double) defectCount2 / n;

      // Rule 3: Use "measured force" — Defect if the opponent's defection rate exceeds 6% forgiveness threshold
      if (defectRate1 >= 0.06 || defectRate2 >= 0.06) return 1;

      // Rule 4 : Don’t hold grudges — cooperate immediately when both opponents cooperate
      return 0;
   }
}
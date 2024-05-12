# Maze_Solvers

A projekt fő feladata egy labirintus generálása, majd a labirintusból való kijutás 3-féle módszerrel való megoldása. Minden esetben egy 20x20-as négyzetrács, mint labirintus bal felső pontja a kiindulási pont, és a jobb alsó pont a cél.

A labirintus generálása egy DFS-fa létrehozásával történik. Az egyik megoldási módszer is DFS-módszerrel történik. Egy másik megoldásunk a balkéz-szabállyal történik, amely során végig a bal kezünket egy falon tartjuk. A harmadik módszer pedig Trémaux-algoritmusán alapszik, amelynek a következő a lényege. Ha egy kereszteződéshez ér az ember a labirintusban, akkor megjelöli ahol odajutott, illetve a kijáratot is. Ha egy kerszteződésnél csak a bejárat van megjelölve, akkor bármelyik kijáratot lehet választani. Egyébként válassza a bejáratot a továbbhaladáshoz, kivéve ha már kétszer meg van jelölve. Ez esetben a legkevesebb jelöléssel rendelkező kijáratot kell választani.

SQLite format 3   @     �              $                                                 � .O}� � �@��                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 �&�/tablepostpostCREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  deleted TIMESTAMP DEFAULT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
)P++Ytablesqlite_sequencesqlite_sequenceCREATE TABLE sqlite_sequence(name,seq)��{tableuseruserCREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
)'; indexsqlite_autoindex_user_1user          � ��>�`�                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          n �YABCpbkdf2:sha256:260000$q88n1GW3xfQqcBVa$296ceea1644ac5e587b70b3f40d0c37138b671eb4f0a9d4e349e71a74dcbd8ccl �Yapbkdf2:sha256:260000$HOXidDxtA1MALQj9$051c25eadac62d232db7d27f5b8678a1963f7654ca6f234ad2b9b708aea4c33cn �Ydfspbkdf2:sha256:260000$maPNwhTuSQOH4dL0$aa622af5aba6e7e7b012c247efe0fd79b854f88019d7de732a2e1326e626677an �Ybcdpbkdf2:sha256:260000$vryHqvWTcuaby12M$d9e3d24a81fc13e08b21e162edbfda7741127d98f7de5a0510cb4ac6b3f27d5bn �Ybcepbkdf2:sha256:260000$zxWwVT1vGOGffHkM$16075b1c1a8b2c515336bdd654e10ab1af61751798dbe280f2db1a21f6f9662fp �Yoreespbkdf2:sha256:260000$ptm1HhwNbqUdhMYf$d1cc1e8194ac9bc87c25ac38d1d6870fad23ee624219e8935f847e613942c1cdn �Yabcpbkdf2:sha256:260000$5Lelf746d3cGsr8f$ff36f2adccdda1f303a8567e2968fa0c2b170ab3d8d3370718ed46b759fcd19f
   � �������                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   ABCadfsbcdbce	orees	abc� � ��                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        post	       user� 	� ��eI�s��3                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 F 3732023-04-02 20:07:26Something new in lifenen2023-04-02 20:29:010	 332023-04-02 20:28:16aa2023-04-02 20:29:001 33 2023-04-02 17:01:40abcabcdefgh
Some more 3 2023-03-31 20:02:2311* ;43 37 2023-04-02 20:07:26Something new in lifenen6 332023-03-30 16:38:18fadsfads2023-03-30 16:38:20   3 2023-04-02 20:28:16aa( 3! 2023-03-31 19:58:17abcFormer ABC3 3!) 2023-03-31 20:08:13Some real Some fake some3 	332023-03-30 16:21:05abcabc2023-03-30 16:23:00! 3 2023-03-30 16:20:49abcabc
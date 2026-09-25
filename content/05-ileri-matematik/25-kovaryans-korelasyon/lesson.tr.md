# Kovaryans ve Korelasyon

Şimdiye kadar değişkenlere tek tek baktık: ortalaması, varyansı,
dağılımı. Ama veri bilimindeki soruların çoğu iki değişkenin **birlikte**
nasıl davrandığıyla ilgili: boy uzadıkça kilo artıyor mu, reklam harcaması
satışla birlikte mi yükseliyor, iki özellik aynı bilgiyi mi taşıyor? Bu
bölümde bu birlikteliği ölçen iki sayıyı, **kovaryansı** ve
**korelasyonu**, sonra da çok değişkenli verinin özeti olan **kovaryans
matrisini** göreceğiz.

Ön bilgi: Rastgele Değişkenler, Beklenen Değer ve Varyans; MAT 1'deki Veri
ve Temel İstatistik.

## Saçılım grafiği

İki değişkenli veriye ilk bakış **saçılım grafiğidir**: her gözlem bir
nokta, $x$ bir değişken, $y$ öteki.

<figure class="fig">
<svg viewBox="0 0 440 330" width="440"><rect class="box" opacity="1" x="30.0" y="26.0" width="175.0" height="105.0"/><circle class="dot" cx="177.0" cy="58.9" r="2.6"/><circle class="dot" cx="43.0" cy="118.3" r="2.6"/><circle class="dot" cx="129.7" cy="79.3" r="2.6"/><circle class="dot" cx="100.9" cy="81.7" r="2.6"/><circle class="dot" cx="104.3" cy="101.1" r="2.6"/><circle class="dot" cx="111.2" cy="88.9" r="2.6"/><circle class="dot" cx="58.6" cy="104.9" r="2.6"/><circle class="dot" cx="110.7" cy="73.3" r="2.6"/><circle class="dot" cx="92.3" cy="108.6" r="2.6"/><circle class="dot" cx="124.1" cy="72.4" r="2.6"/><circle class="dot" cx="107.2" cy="88.7" r="2.6"/><circle class="dot" cx="109.3" cy="70.8" r="2.6"/><circle class="dot" cx="98.0" cy="98.1" r="2.6"/><circle class="dot" cx="86.7" cy="92.4" r="2.6"/><circle class="dot" cx="106.1" cy="92.7" r="2.6"/><circle class="dot" cx="131.6" cy="60.2" r="2.6"/><circle class="dot" cx="110.5" cy="82.4" r="2.6"/><circle class="dot" cx="145.4" cy="66.3" r="2.6"/><circle class="dot" cx="111.7" cy="94.8" r="2.6"/><circle class="dot" cx="118.2" cy="65.3" r="2.6"/><circle class="dot" cx="162.6" cy="48.4" r="2.6"/><circle class="dot" cx="133.4" cy="64.2" r="2.6"/><circle class="dot" cx="102.8" cy="77.8" r="2.6"/><circle class="dot" cx="112.2" cy="78.7" r="2.6"/><circle class="dot" cx="133.3" cy="74.9" r="2.6"/><circle class="dot" cx="173.9" cy="54.1" r="2.6"/><circle class="dot" cx="109.6" cy="88.9" r="2.6"/><circle class="dot" cx="110.4" cy="71.9" r="2.6"/><circle class="dot" cx="146.7" cy="73.9" r="2.6"/><circle class="dot" cx="91.6" cy="97.0" r="2.6"/><circle class="dot" cx="109.0" cy="85.5" r="2.6"/><circle class="dot" cx="143.2" cy="62.9" r="2.6"/><circle class="dot" cx="134.4" cy="65.0" r="2.6"/><circle class="dot" cx="120.2" cy="86.6" r="2.6"/><circle class="dot" cx="137.0" cy="81.1" r="2.6"/><circle class="dot" cx="35.0" cy="123.1" r="2.6"/><circle class="dot" cx="147.3" cy="53.2" r="2.6"/><circle class="dot" cx="89.5" cy="87.8" r="2.6"/><circle class="dot" cx="68.8" cy="103.1" r="2.6"/><circle class="dot" cx="125.6" cy="76.6" r="2.6"/><circle class="dot" cx="137.9" cy="65.2" r="2.6"/><circle class="dot" cx="104.5" cy="87.4" r="2.6"/><circle class="dot" cx="86.1" cy="89.2" r="2.6"/><circle class="dot" cx="118.3" cy="84.1" r="2.6"/><circle class="dot" cx="116.0" cy="78.3" r="2.6"/><circle class="dot" cx="158.5" cy="57.2" r="2.6"/><circle class="dot" cx="139.3" cy="62.6" r="2.6"/><circle class="dot" cx="123.2" cy="73.7" r="2.6"/><circle class="dot" cx="149.9" cy="41.5" r="2.6"/><circle class="dot" cx="111.5" cy="70.3" r="2.6"/><circle class="dot" cx="90.5" cy="81.7" r="2.6"/><circle class="dot" cx="134.5" cy="84.9" r="2.6"/><circle class="dot" cx="134.5" cy="71.9" r="2.6"/><circle class="dot" cx="111.2" cy="86.5" r="2.6"/><circle class="dot" cx="94.7" cy="86.8" r="2.6"/><circle class="dot" cx="124.2" cy="92.3" r="2.6"/><circle class="dot" cx="44.8" cy="108.8" r="2.6"/><circle class="dot" cx="137.6" cy="59.5" r="2.6"/><circle class="dot" cx="131.8" cy="80.7" r="2.6"/><text class="ink" x="117" y="18" font-size="11" text-anchor="middle">güçlü pozitif</text><text class="ink" x="117" y="147" font-size="11" text-anchor="middle">r = 0,88</text><rect class="box" opacity="1" x="235.0" y="26.0" width="175.0" height="105.0"/><circle class="dot" cx="347.5" cy="73.8" r="2.6"/><circle class="dot" cx="353.3" cy="64.8" r="2.6"/><circle class="dot" cx="282.1" cy="104.4" r="2.6"/><circle class="dot" cx="281.4" cy="50.3" r="2.6"/><circle class="dot" cx="340.1" cy="86.7" r="2.6"/><circle class="dot" cx="321.6" cy="56.4" r="2.6"/><circle class="dot" cx="287.2" cy="77.1" r="2.6"/><circle class="dot" cx="313.9" cy="85.3" r="2.6"/><circle class="dot" cx="319.4" cy="81.0" r="2.6"/><circle class="dot" cx="318.3" cy="62.8" r="2.6"/><circle class="dot" cx="346.6" cy="93.6" r="2.6"/><circle class="dot" cx="333.7" cy="85.1" r="2.6"/><circle class="dot" cx="374.1" cy="86.9" r="2.6"/><circle class="dot" cx="362.6" cy="108.5" r="2.6"/><circle class="dot" cx="342.3" cy="55.7" r="2.6"/><circle class="dot" cx="353.9" cy="68.4" r="2.6"/><circle class="dot" cx="361.1" cy="78.9" r="2.6"/><circle class="dot" cx="343.1" cy="58.1" r="2.6"/><circle class="dot" cx="286.7" cy="95.2" r="2.6"/><circle class="dot" cx="347.6" cy="79.8" r="2.6"/><circle class="dot" cx="324.6" cy="48.3" r="2.6"/><circle class="dot" cx="369.7" cy="61.4" r="2.6"/><circle class="dot" cx="325.2" cy="117.4" r="2.6"/><circle class="dot" cx="332.1" cy="96.7" r="2.6"/><circle class="dot" cx="371.5" cy="59.9" r="2.6"/><circle class="dot" cx="327.7" cy="86.8" r="2.6"/><circle class="dot" cx="314.6" cy="82.3" r="2.6"/><circle class="dot" cx="331.5" cy="67.9" r="2.6"/><circle class="dot" cx="309.7" cy="94.0" r="2.6"/><circle class="dot" cx="327.2" cy="74.8" r="2.6"/><circle class="dot" cx="322.3" cy="64.6" r="2.6"/><circle class="dot" cx="330.4" cy="70.3" r="2.6"/><circle class="dot" cx="378.6" cy="71.6" r="2.6"/><circle class="dot" cx="310.7" cy="89.0" r="2.6"/><circle class="dot" cx="323.6" cy="69.5" r="2.6"/><circle class="dot" cx="316.7" cy="86.0" r="2.6"/><circle class="dot" cx="342.1" cy="55.7" r="2.6"/><circle class="dot" cx="288.0" cy="33.5" r="2.6"/><circle class="dot" cx="302.3" cy="91.4" r="2.6"/><circle class="dot" cx="321.3" cy="116.6" r="2.6"/><circle class="dot" cx="338.4" cy="85.9" r="2.6"/><circle class="dot" cx="321.2" cy="71.9" r="2.6"/><circle class="dot" cx="307.9" cy="60.1" r="2.6"/><circle class="dot" cx="297.2" cy="59.6" r="2.6"/><circle class="dot" cx="337.4" cy="92.2" r="2.6"/><circle class="dot" cx="364.6" cy="92.4" r="2.6"/><circle class="dot" cx="331.9" cy="56.3" r="2.6"/><circle class="dot" cx="328.0" cy="97.6" r="2.6"/><circle class="dot" cx="335.4" cy="59.4" r="2.6"/><circle class="dot" cx="295.0" cy="82.5" r="2.6"/><circle class="dot" cx="313.4" cy="65.1" r="2.6"/><circle class="dot" cx="314.7" cy="66.1" r="2.6"/><circle class="dot" cx="331.1" cy="64.9" r="2.6"/><circle class="dot" cx="321.6" cy="64.1" r="2.6"/><circle class="dot" cx="287.0" cy="95.8" r="2.6"/><circle class="dot" cx="355.3" cy="73.3" r="2.6"/><circle class="dot" cx="371.9" cy="78.3" r="2.6"/><circle class="dot" cx="314.8" cy="73.1" r="2.6"/><circle class="dot" cx="334.1" cy="56.9" r="2.6"/><text class="ink" x="322" y="18" font-size="11" text-anchor="middle">ilişki yok</text><text class="ink" x="322" y="147" font-size="11" text-anchor="middle">r = −0,01</text><rect class="box" opacity="1" x="30.0" y="176.0" width="175.0" height="105.0"/><circle class="dot" cx="109.6" cy="225.5" r="2.6"/><circle class="dot" cx="96.7" cy="226.1" r="2.6"/><circle class="dot" cx="96.3" cy="237.8" r="2.6"/><circle class="dot" cx="108.4" cy="229.0" r="2.6"/><circle class="dot" cx="139.5" cy="263.8" r="2.6"/><circle class="dot" cx="93.7" cy="225.8" r="2.6"/><circle class="dot" cx="151.3" cy="233.1" r="2.6"/><circle class="dot" cx="126.0" cy="211.8" r="2.6"/><circle class="dot" cx="110.9" cy="213.7" r="2.6"/><circle class="dot" cx="78.7" cy="223.0" r="2.6"/><circle class="dot" cx="124.6" cy="225.3" r="2.6"/><circle class="dot" cx="137.7" cy="246.8" r="2.6"/><circle class="dot" cx="66.0" cy="196.6" r="2.6"/><circle class="dot" cx="152.3" cy="244.5" r="2.6"/><circle class="dot" cx="165.6" cy="238.0" r="2.6"/><circle class="dot" cx="127.4" cy="200.5" r="2.6"/><circle class="dot" cx="131.8" cy="223.0" r="2.6"/><circle class="dot" cx="187.9" cy="228.9" r="2.6"/><circle class="dot" cx="153.4" cy="241.4" r="2.6"/><circle class="dot" cx="91.3" cy="221.6" r="2.6"/><circle class="dot" cx="117.0" cy="211.6" r="2.6"/><circle class="dot" cx="112.9" cy="205.0" r="2.6"/><circle class="dot" cx="113.1" cy="233.6" r="2.6"/><circle class="dot" cx="48.5" cy="198.6" r="2.6"/><circle class="dot" cx="139.6" cy="255.7" r="2.6"/><circle class="dot" cx="98.9" cy="223.2" r="2.6"/><circle class="dot" cx="122.3" cy="219.4" r="2.6"/><circle class="dot" cx="113.5" cy="227.9" r="2.6"/><circle class="dot" cx="142.9" cy="246.3" r="2.6"/><circle class="dot" cx="108.9" cy="242.5" r="2.6"/><circle class="dot" cx="94.3" cy="214.2" r="2.6"/><circle class="dot" cx="133.0" cy="225.1" r="2.6"/><circle class="dot" cx="158.5" cy="238.3" r="2.6"/><circle class="dot" cx="108.2" cy="221.4" r="2.6"/><circle class="dot" cx="157.5" cy="261.2" r="2.6"/><circle class="dot" cx="125.1" cy="209.7" r="2.6"/><circle class="dot" cx="102.0" cy="222.7" r="2.6"/><circle class="dot" cx="162.0" cy="249.0" r="2.6"/><circle class="dot" cx="93.6" cy="209.3" r="2.6"/><circle class="dot" cx="147.1" cy="268.0" r="2.6"/><circle class="dot" cx="103.0" cy="223.2" r="2.6"/><circle class="dot" cx="130.6" cy="235.7" r="2.6"/><circle class="dot" cx="81.5" cy="208.7" r="2.6"/><circle class="dot" cx="93.1" cy="201.4" r="2.6"/><circle class="dot" cx="148.6" cy="235.6" r="2.6"/><circle class="dot" cx="123.0" cy="253.7" r="2.6"/><circle class="dot" cx="118.6" cy="233.2" r="2.6"/><circle class="dot" cx="104.7" cy="220.5" r="2.6"/><circle class="dot" cx="130.5" cy="232.1" r="2.6"/><circle class="dot" cx="76.7" cy="227.4" r="2.6"/><circle class="dot" cx="84.8" cy="235.6" r="2.6"/><circle class="dot" cx="112.9" cy="219.7" r="2.6"/><circle class="dot" cx="93.2" cy="214.0" r="2.6"/><circle class="dot" cx="97.1" cy="220.2" r="2.6"/><circle class="dot" cx="115.4" cy="249.2" r="2.6"/><circle class="dot" cx="113.5" cy="204.6" r="2.6"/><circle class="dot" cx="111.0" cy="262.0" r="2.6"/><circle class="dot" cx="166.1" cy="253.4" r="2.6"/><circle class="dot" cx="147.0" cy="214.8" r="2.6"/><circle class="dot" cx="153.4" cy="245.5" r="2.6"/><text class="ink" x="117" y="168" font-size="11" text-anchor="middle">orta negatif</text><text class="ink" x="117" y="297" font-size="11" text-anchor="middle">r = −0,56</text><rect class="box" opacity="1" x="235.0" y="176.0" width="175.0" height="105.0"/><circle class="dot" cx="264.2" cy="180.6" r="2.6"/><circle class="dot" cx="266.1" cy="189.0" r="2.6"/><circle class="dot" cx="268.1" cy="186.9" r="2.6"/><circle class="dot" cx="270.1" cy="198.2" r="2.6"/><circle class="dot" cx="272.1" cy="198.3" r="2.6"/><circle class="dot" cx="274.1" cy="202.6" r="2.6"/><circle class="dot" cx="276.0" cy="209.6" r="2.6"/><circle class="dot" cx="278.0" cy="208.2" r="2.6"/><circle class="dot" cx="280.0" cy="217.8" r="2.6"/><circle class="dot" cx="282.0" cy="219.2" r="2.6"/><circle class="dot" cx="283.9" cy="220.7" r="2.6"/><circle class="dot" cx="285.9" cy="224.8" r="2.6"/><circle class="dot" cx="287.9" cy="225.4" r="2.6"/><circle class="dot" cx="289.9" cy="226.9" r="2.6"/><circle class="dot" cx="291.9" cy="232.7" r="2.6"/><circle class="dot" cx="293.8" cy="235.8" r="2.6"/><circle class="dot" cx="295.8" cy="237.9" r="2.6"/><circle class="dot" cx="297.8" cy="239.6" r="2.6"/><circle class="dot" cx="299.8" cy="238.5" r="2.6"/><circle class="dot" cx="301.7" cy="243.0" r="2.6"/><circle class="dot" cx="303.7" cy="242.9" r="2.6"/><circle class="dot" cx="305.7" cy="245.7" r="2.6"/><circle class="dot" cx="307.7" cy="248.9" r="2.6"/><circle class="dot" cx="309.6" cy="245.6" r="2.6"/><circle class="dot" cx="311.6" cy="251.5" r="2.6"/><circle class="dot" cx="313.6" cy="249.6" r="2.6"/><circle class="dot" cx="315.6" cy="246.4" r="2.6"/><circle class="dot" cx="317.6" cy="253.6" r="2.6"/><circle class="dot" cx="319.5" cy="251.2" r="2.6"/><circle class="dot" cx="321.5" cy="255.4" r="2.6"/><circle class="dot" cx="323.5" cy="252.6" r="2.6"/><circle class="dot" cx="325.5" cy="255.0" r="2.6"/><circle class="dot" cx="327.4" cy="251.7" r="2.6"/><circle class="dot" cx="329.4" cy="251.7" r="2.6"/><circle class="dot" cx="331.4" cy="249.3" r="2.6"/><circle class="dot" cx="333.4" cy="244.7" r="2.6"/><circle class="dot" cx="335.4" cy="247.1" r="2.6"/><circle class="dot" cx="337.3" cy="245.0" r="2.6"/><circle class="dot" cx="339.3" cy="245.6" r="2.6"/><circle class="dot" cx="341.3" cy="244.6" r="2.6"/><circle class="dot" cx="343.3" cy="244.6" r="2.6"/><circle class="dot" cx="345.2" cy="245.3" r="2.6"/><circle class="dot" cx="347.2" cy="238.5" r="2.6"/><circle class="dot" cx="349.2" cy="232.3" r="2.6"/><circle class="dot" cx="351.2" cy="233.1" r="2.6"/><circle class="dot" cx="353.1" cy="233.3" r="2.6"/><circle class="dot" cx="355.1" cy="225.0" r="2.6"/><circle class="dot" cx="357.1" cy="227.8" r="2.6"/><circle class="dot" cx="359.1" cy="225.3" r="2.6"/><circle class="dot" cx="361.1" cy="223.8" r="2.6"/><circle class="dot" cx="363.0" cy="220.0" r="2.6"/><circle class="dot" cx="365.0" cy="214.7" r="2.6"/><circle class="dot" cx="367.0" cy="205.3" r="2.6"/><circle class="dot" cx="369.0" cy="207.4" r="2.6"/><circle class="dot" cx="370.9" cy="205.7" r="2.6"/><circle class="dot" cx="372.9" cy="200.5" r="2.6"/><circle class="dot" cx="374.9" cy="195.3" r="2.6"/><circle class="dot" cx="376.9" cy="194.9" r="2.6"/><circle class="dot" cx="378.9" cy="185.6" r="2.6"/><circle class="dot" cx="380.8" cy="179.4" r="2.6"/><text class="ink" x="322" y="168" font-size="11" text-anchor="middle">ilişki var, ama doğrusal değil</text><text class="ink" x="322" y="297" font-size="11" text-anchor="middle">r = 0,00</text></svg>
  <figcaption>Dört veri kümesi ve korelasyonları. Noktalar yukarı doğru bir şerit oluşturuyorsa r pozitif, aşağı doğruysa negatif. Sağ alttaki kümede y tamamen x'e bağlı, ama ilişki doğrusal olmadığı için r yaklaşık 0.</figcaption>
</figure>

## Kovaryans

Bir noktanın ortalamalardan sapmalarını çarpalım:
$(x - \bar{x})(y - \bar{y})$.

- İki sapma aynı işaretliyse (ikisi de ortalamanın üstünde ya da ikisi de
  altında) çarpım **pozitif**.
- Zıt işaretliyse **negatif**.

<figure class="fig">
<svg viewBox="0 0 440 262" width="440"><line class="grid" x1="40.0" y1="240.0" x2="40.0" y2="20.0"/><line class="grid" x1="74.0" y1="240.0" x2="74.0" y2="20.0"/><line class="grid" x1="108.0" y1="240.0" x2="108.0" y2="20.0"/><line class="grid" x1="142.0" y1="240.0" x2="142.0" y2="20.0"/><line class="grid" x1="176.0" y1="240.0" x2="176.0" y2="20.0"/><line class="grid" x1="210.0" y1="240.0" x2="210.0" y2="20.0"/><line class="grid" x1="244.0" y1="240.0" x2="244.0" y2="20.0"/><line class="grid" x1="278.0" y1="240.0" x2="278.0" y2="20.0"/><line class="grid" x1="312.0" y1="240.0" x2="312.0" y2="20.0"/><line class="grid" x1="346.0" y1="240.0" x2="346.0" y2="20.0"/><line class="grid" x1="380.0" y1="240.0" x2="380.0" y2="20.0"/><line class="grid" x1="40.0" y1="240.0" x2="380.0" y2="240.0"/><line class="grid" x1="40.0" y1="218.0" x2="380.0" y2="218.0"/><line class="grid" x1="40.0" y1="196.0" x2="380.0" y2="196.0"/><line class="grid" x1="40.0" y1="174.0" x2="380.0" y2="174.0"/><line class="grid" x1="40.0" y1="152.0" x2="380.0" y2="152.0"/><line class="grid" x1="40.0" y1="130.0" x2="380.0" y2="130.0"/><line class="grid" x1="40.0" y1="108.0" x2="380.0" y2="108.0"/><line class="grid" x1="40.0" y1="86.0" x2="380.0" y2="86.0"/><line class="grid" x1="40.0" y1="64.0" x2="380.0" y2="64.0"/><line class="grid" x1="40.0" y1="42.0" x2="380.0" y2="42.0"/><line class="grid" x1="40.0" y1="20.0" x2="380.0" y2="20.0"/><rect class="dot3" opacity="0.1" x="207.0" y="20.0" width="173.0" height="113.5"/><rect class="dot3" opacity="0.1" x="40.0" y="133.5" width="167.0" height="106.5"/><rect class="dot2" opacity="0.1" x="40.0" y="20.0" width="167.0" height="113.5"/><rect class="dot2" opacity="0.1" x="207.0" y="133.5" width="173.0" height="106.5"/><line class="curve3" stroke-dasharray="5 4" x1="207.0" y1="240.0" x2="207.0" y2="20.0"/><line class="curve3" stroke-dasharray="5 4" x1="40.0" y1="133.5" x2="380.0" y2="133.5"/><circle class="dot2" cx="211.9" cy="139.4" r="4"/><circle class="dot3" cx="284.0" cy="122.7" r="4"/><circle class="dot3" cx="276.6" cy="132.7" r="4"/><circle class="dot3" cx="182.2" cy="141.8" r="4"/><circle class="dot2" cx="193.8" cy="117.6" r="4"/><circle class="dot3" cx="181.3" cy="148.1" r="4"/><circle class="dot3" cx="241.0" cy="132.3" r="4"/><circle class="dot2" cx="207.0" cy="122.9" r="4"/><circle class="dot3" cx="250.6" cy="95.8" r="4"/><circle class="dot3" cx="109.5" cy="182.1" r="4"/><circle class="dot3" cx="295.2" cy="79.4" r="4"/><circle class="dot2" cx="204.8" cy="109.4" r="4"/><circle class="dot3" cx="247.0" cy="117.8" r="4"/><circle class="dot3" cx="202.6" cy="151.3" r="4"/><circle class="dot2" cx="189.4" cy="131.7" r="4"/><circle class="dot3" cx="235.2" cy="113.1" r="4"/><circle class="dot3" cx="254.9" cy="85.5" r="4"/><circle class="dot3" cx="199.0" cy="163.3" r="4"/><circle class="dot3" cx="201.7" cy="148.3" r="4"/><circle class="dot3" cx="247.3" cy="131.5" r="4"/><circle class="dot3" cx="162.7" cy="189.6" r="4"/><circle class="dot3" cx="127.6" cy="164.5" r="4"/><circle class="dot3" cx="231.5" cy="108.7" r="4"/><circle class="dot3" cx="173.5" cy="162.8" r="4"/><circle class="dot3" cx="105.5" cy="146.8" r="4"/><circle class="dot2" cx="165.7" cy="132.0" r="4"/><text class="ink" x="207.0" y="256.0" font-size="12" text-anchor="middle">x̄</text><text class="ink" x="34.0" y="137.5" font-size="12" text-anchor="end">ȳ</text><text class="ink" x="373.2" y="34.8" font-size="11" text-anchor="end">çarpım +</text><text class="ink" x="46.8" y="229.2" font-size="11" text-anchor="start">çarpım +</text><text class="ink" x="46.8" y="34.8" font-size="11" text-anchor="start">çarpım −</text><text class="ink" x="373.2" y="229.2" font-size="11" text-anchor="end">çarpım −</text></svg>
  <figcaption>Kesikli çizgiler ortalamalar. Sağ üst ve sol alttaki noktalarda çarpım pozitif (yeşil), öteki iki bölgede negatif (turuncu). Yeşiller ağır bastığı için kovaryans pozitif.</figcaption>
</figure>

**Kovaryans** bu çarpımların ortalamasıdır:

$$
\operatorname{Cov}(X, Y) = E\big[(X - \mu_X)(Y - \mu_Y)\big] = E[XY] - E[X]\,E[Y]
$$

Örneklemde, varyanstaki gibi $n - 1$'e bölünür:

$$
s_{xy} = \frac{1}{n - 1} \sum_{i=1}^{n} (x_i - \bar{x})(y_i - \bar{y})
$$

**Örnek.** $x = 1, 2, 3, 4, 5$ ve $y = 2, 4, 5, 4, 5$. $\bar{x} = 3$,
$\bar{y} = 4$. Sapmalar: $x$ için $-2, -1, 0, 1, 2$; $y$ için
$-2, 0, 1, 0, 1$. Çarpımlar $4, 0, 0, 0, 2$; toplam $6$.
$s_{xy} = \frac{6}{4} = 1{,}5$.

**Kovaryansın sorunu: birim.** Boyu santimetre yerine metreyle ölçersek
kovaryans $100$ kat küçülür; ilişki değişmediği hâlde. Kovaryansın
işareti anlamlı, büyüklüğü tek başına yorumlanamaz.

## Korelasyon

Kovaryansı iki standart sapmaya bölünce birimsiz bir sayı elde edilir,
**korelasyon katsayısı** (Pearson):

$$
r = \frac{s_{xy}}{s_x \, s_y}
$$

- $-1 \leq r \leq 1$.
- $r = 1$: bütün noktalar artan bir doğru üzerinde; $r = -1$: azalan bir
  doğru üzerinde.
- $r \approx 0$: **doğrusal** bir ilişki yok.

Başka bir bakış: $r$, iki değişkenin z skorlarının çarpımlarının
ortalamasıdır ($n - 1$'e bölerek).

**Örnek (devam).** $s_x^2 = \frac{4 + 1 + 0 + 1 + 4}{4} = 2{,}5$,
$s_y^2 = \frac{4 + 0 + 1 + 0 + 1}{4} = 1{,}5$.
$r = \frac{1{,}5}{\sqrt{2{,}5 \cdot 1{,}5}} = \frac{1{,}5}{\sqrt{3{,}75}}
\approx 0{,}775$.

**Kabaca yorum.** $|r| < 0{,}3$ zayıf, $0{,}3$–$0{,}7$ orta, $> 0{,}7$
güçlü. Bu sınırlar alana göre değişir; fizikte $0{,}9$ zayıf sayılabilir,
psikolojide $0{,}4$ güçlü.

## Kurallar

- $\operatorname{Cov}(X, X) = \operatorname{Var}(X)$.
- $\operatorname{Cov}(X, Y) = \operatorname{Cov}(Y, X)$.
- $\operatorname{Cov}(aX + b, \ cY + d) = ac \operatorname{Cov}(X, Y)$;
  sabit eklemek kovaryansı değiştirmez.
- Korelasyon birim değişikliğinden etkilenmez: $a$ ve $c$ aynı işaretliyse
  $r$ aynı kalır, zıt işaretliyse yalnızca işareti değişir.
- Toplamın varyansı:

$$
\operatorname{Var}(X \pm Y) = \operatorname{Var}(X) + \operatorname{Var}(Y) \pm 2\operatorname{Cov}(X, Y)
$$

Bağımsızlıkta kovaryans $0$ olduğu için Rastgele Değişkenler bölümündeki
"varyanslar toplanır" kuralı buradan çıkar.

**Bağımsız ⇒ kovaryans 0, ama tersi doğru değil.** $X$, $-1$, $0$, $1$
değerlerini eşit olasılıkla alsın ve $Y = X^2$ olsun. $Y$ tamamen $X$'e
bağlı; ama $E[XY] = E[X^3] = 0$ ve $E[X] = 0$, yani
$\operatorname{Cov}(X, Y) = 0$. Korelasyon yalnızca doğrusal ilişkiyi
görür.

## Korelasyon nedensellik değildir

Dondurma satışları ile boğulma vakaları arasında pozitif korelasyon var;
dondurma boğulmaya yol açmaz. İkisini de sıcak hava artırır: gizli bir
**üçüncü değişken**. Korelasyondan nedensellik çıkarmak için kontrollü
deney (rastgele atama, A/B testi gibi) gerekir.

<figure class="fig">
<svg viewBox="0 0 440 268" width="440"><line class="grid" x1="40.0" y1="220.0" x2="40.0" y2="20.0"/><line class="grid" x1="82.5" y1="220.0" x2="82.5" y2="20.0"/><line class="grid" x1="125.0" y1="220.0" x2="125.0" y2="20.0"/><line class="grid" x1="167.5" y1="220.0" x2="167.5" y2="20.0"/><line class="grid" x1="210.0" y1="220.0" x2="210.0" y2="20.0"/><line class="grid" x1="252.5" y1="220.0" x2="252.5" y2="20.0"/><line class="grid" x1="295.0" y1="220.0" x2="295.0" y2="20.0"/><line class="grid" x1="337.5" y1="220.0" x2="337.5" y2="20.0"/><line class="grid" x1="380.0" y1="220.0" x2="380.0" y2="20.0"/><line class="grid" x1="40.0" y1="220.0" x2="380.0" y2="220.0"/><line class="grid" x1="40.0" y1="193.3" x2="380.0" y2="193.3"/><line class="grid" x1="40.0" y1="166.7" x2="380.0" y2="166.7"/><line class="grid" x1="40.0" y1="140.0" x2="380.0" y2="140.0"/><line class="grid" x1="40.0" y1="113.3" x2="380.0" y2="113.3"/><line class="grid" x1="40.0" y1="86.7" x2="380.0" y2="86.7"/><line class="grid" x1="40.0" y1="60.0" x2="380.0" y2="60.0"/><line class="grid" x1="40.0" y1="33.3" x2="380.0" y2="33.3"/><line class="line" x1="40.0" y1="220.0" x2="380.0" y2="220.0"/><line class="line" x1="40.0" y1="220.0" x2="40.0" y2="20.0"/><text class="dim" x="82.5" y="233.0" font-size="9" text-anchor="middle">2</text><text class="dim" x="125.0" y="233.0" font-size="9" text-anchor="middle">4</text><text class="dim" x="167.5" y="233.0" font-size="9" text-anchor="middle">6</text><text class="dim" x="210.0" y="233.0" font-size="9" text-anchor="middle">8</text><text class="dim" x="252.5" y="233.0" font-size="9" text-anchor="middle">10</text><text class="dim" x="295.0" y="233.0" font-size="9" text-anchor="middle">12</text><text class="dim" x="337.5" y="233.0" font-size="9" text-anchor="middle">14</text><text class="dim" x="380.0" y="233.0" font-size="9" text-anchor="middle">16</text><text class="dim" x="35.0" y="196.3" font-size="9" text-anchor="end">2</text><text class="dim" x="35.0" y="169.7" font-size="9" text-anchor="end">4</text><text class="dim" x="35.0" y="143.0" font-size="9" text-anchor="end">6</text><text class="dim" x="35.0" y="116.3" font-size="9" text-anchor="end">8</text><text class="dim" x="35.0" y="89.7" font-size="9" text-anchor="end">10</text><text class="dim" x="35.0" y="63.0" font-size="9" text-anchor="end">12</text><text class="dim" x="35.0" y="36.3" font-size="9" text-anchor="end">14</text><circle class="dot" cx="61.2" cy="166.7" r="4"/><circle class="dot" cx="82.5" cy="193.3" r="4"/><circle class="dot" cx="103.8" cy="153.3" r="4"/><circle class="dot" cx="125.0" cy="180.0" r="4"/><circle class="dot" cx="146.2" cy="193.3" r="4"/><circle class="dot" cx="167.5" cy="153.3" r="4"/><circle class="dot" cx="188.8" cy="180.0" r="4"/><circle class="dot" cx="210.0" cy="166.7" r="4"/><circle class="dot2" cx="358.8" cy="33.3" r="5"/><text class="ink" x="348.8" y="37.3" font-size="11" text-anchor="end">aykırı değer</text><text class="ink" x="140" y="256" font-size="12" text-anchor="middle">onsuz: r = 0,10</text><text class="ink" x="290" y="256" font-size="12" text-anchor="middle">onunla: r = 0,81</text></svg>
  <figcaption>Sekiz noktanın arasında belirgin bir ilişki yok (r ≈ 0,10). Tek bir aykırı değer eklenince r 0,81'e çıkıyor. Korelasyon hesaplamadan önce saçılım grafiğine bakmak gerekir.</figcaption>
</figure>

**Aykırı değerler.** $r$, ortalama ve standart sapma gibi aykırı değerlere
duyarlıdır. Aykırı değerler varsa ya da ilişki monoton ama doğrusal
değilse, değerlerin kendisi yerine **sıralarının** korelasyonu
(**Spearman**) kullanılabilir.

## Kovaryans matrisi

$d$ özellikli bir veride her özellik çiftinin kovaryansı bir $d \times d$
matriste toplanır:

$$
\Sigma_{ij} = \operatorname{Cov}(X_i, X_j)
$$

- Köşegende varyanslar, köşegen dışında kovaryanslar.
- Simetrik: $\Sigma_{ij} = \Sigma_{ji}$.
- Pozitif yarı tanımlı: her $w$ için $w^\mathsf{T} \Sigma w =
  \operatorname{Var}(w^\mathsf{T} X) \geq 0$; bir varyans negatif olamaz.

Veri matrisi $X$ ($n \times d$) sütun ortalamaları çıkarılarak
merkezlenirse:

$$
\Sigma = \frac{1}{n - 1} X^\mathsf{T} X
$$

Her elemanı standart sapmalara bölünmüş hâli **korelasyon matrisidir**;
köşegeni hep $1$. Özdeğerler bölümünde gördüğümüz gibi simetrik matrislerin
özvektörleri dik; PCA bölümünde kovaryans matrisinin özvektörleri verinin
en çok yayıldığı yönler olacak.

**Örnek.** İki özellik: $\operatorname{Var}(X_1) = 4$,
$\operatorname{Var}(X_2) = 9$, $\operatorname{Cov}(X_1, X_2) = 3$.

$$
\Sigma = \begin{pmatrix} 4 & 3 \\ 3 & 9 \end{pmatrix} \qquad
r = \frac{3}{2 \cdot 3} = 0{,}5
$$

## Makine öğrenmesinde

**Özellikler arası korelasyon.** Birbiriyle çok yüksek korelasyonlu iki
özellik (metrekare ve oda sayısı gibi) büyük ölçüde aynı bilgiyi taşır.
Doğrusal modellerde bu **çoklu doğrusallık**, katsayıları kararsız yapar.
Korelasyon matrisi bu çiftleri bulmanın ilk aracıdır.

**Hedefle korelasyon.** Bir özelliğin hedefle korelasyonu, özellik seçiminde
kaba bir ölçüttür; ama yalnızca doğrusal ilişkiyi görür.

**Topluluk modelleri.** Hataları aynı varyansta ($\sigma^2$) ve
korelasyonu $\rho$ olan iki modelin ortalamasının hata varyansı:

$$
\operatorname{Var}\!\left(\frac{e_1 + e_2}{2}\right) = \frac{\sigma^2 (1 + \rho)}{2}
$$

$\rho = 1$ ise ortalama almak hiç işe yaramaz; $\rho = 0$ ise varyans
yarıya iner. Rastgele ormanların ağaçları birbirinden farklılaştırmaya
çalışmasının nedeni bu.

## Sık yapılan hatalar

<figure class="fig">
  <div class="versus">
    <div class="no">
      <h4>Yanlış</h4>
      <p>r = 0, öyleyse ilişki yok</p>
      <p>korelasyon var, öyleyse neden var</p>
      <p>kovaryans 50, çok güçlü ilişki</p>
      <p>Var(X + Y) = Var(X) + Var(Y) her zaman</p>
    </div>
    <div class="ok">
      <h4>Doğru</h4>
      <p>r = 0: doğrusal ilişki yok</p>
      <p>nedensellik için deney gerekir</p>
      <p>kovaryansın büyüklüğü birime bağlı; r'ye bak</p>
      <p>bağımlılıkta + 2 Cov(X, Y) eklenir</p>
    </div>
  </div>
  <figcaption>Korelasyon tek bir sayı; ilişkinin biçimini görmek için saçılım grafiği şart.</figcaption>
</figure>

- **Eğimle karıştırmak.** $r = 0{,}9$, $y$'nin $x$ ile hızla arttığını
  söylemez; noktaların bir doğruya ne kadar yakın durduğunu söyler. Eğim
  çok küçük olup $r$ yine $1$'e yakın olabilir.

## Özet

- Kovaryans: $\operatorname{Cov}(X, Y) = E[XY] - E[X]E[Y]$; örneklemde
  $\frac{1}{n - 1}\sum (x_i - \bar{x})(y_i - \bar{y})$. İşareti birlikte
  hareketin yönü.
- Korelasyon: $r = \frac{s_{xy}}{s_x s_y}$, $-1$ ile $1$ arası, birimsiz;
  yalnızca doğrusal ilişkiyi ölçer.
- $\operatorname{Var}(X \pm Y) = \operatorname{Var}(X) + \operatorname{Var}(Y)
  \pm 2\operatorname{Cov}(X, Y)$.
- Bağımsız ⇒ kovaryans $0$; tersi doğru değil.
- Korelasyon nedensellik değildir; aykırı değerler $r$'yi çok etkiler.
- Kovaryans matrisi simetrik, pozitif yarı tanımlı;
  $\Sigma = \frac{1}{n - 1} X^\mathsf{T} X$ (merkezlenmiş veri).

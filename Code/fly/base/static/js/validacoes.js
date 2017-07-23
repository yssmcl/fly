function validaCPF(e) {

   var  iLen, iDig0, iDig1, iAux;


    var regex = /(^00*0$)|(^11*1$)|(^22*2$)|(^33*3$)|(^44*4$)|(^55*5$)|(^66*6$)|(^77*7$)|(^88*8$)|(^99*9$)/;
    if (regex.test(e)) {
        return false;
    }

   iLen = e.length;

   if (iLen < 2) {
   	return false;
   }
   else {
   	iDig0 = parseInt(e.substr(iLen - 2, 1), 10);
   	iDig1 = parseInt(e.substr(iLen - 1, 1), 10);
   	// Segundo digito:
   	e = e.substr(0, iLen - 1);
   	iAux = DigitOver(e, 2, 999);
   	if (iAux > 9)
   		iAux = 0;
   	if (iDig1 != iAux) {
   		return false;
   	}
   	else {
   		// Primeiro digito:
   		e = e.substr(0, iLen - 2);
   		iAux = DigitOver(e, 2, 999);
   		if (iAux > 9)
   			iAux = 0;
   		if (iDig0 != iAux) {
   			return false;
   		}
   		else
   			return true;
   	}
   }
}

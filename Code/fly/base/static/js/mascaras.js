// $(document).ready(function(){
//   $("#telefone").mask("(99)99999-9999");
// });

$(document).ready(function(){
	$("input[id$='-cpf']").mask("999.999.999-99");
	$("input[id^='id_main-periodo_']").datepicker();
	$("input[id$='data_nascimento']").datepicker();
});

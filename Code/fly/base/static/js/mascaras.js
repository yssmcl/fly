// $(document).ready(function(){
//   $("#telefone").mask("(99)99999-9999");
// });

$(document).ready(function(){
	// var id = 1;
	// $("#id_membros-" + id + "-cpf").mask("999.999.999-99");
	$("input[id$='-cpf']").mask("999.999.999-99");
});

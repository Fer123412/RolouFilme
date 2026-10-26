const abas = document.querySelectorAll(".aba");
const conteudos = document.querySelectorAll(".aba-conteudo");

abas.forEach((aba) => {
  aba.addEventListener("click", () => {
    abas.forEach((a) => a.classList.remove("ativa"));
    conteudos.forEach((c) => c.classList.remove("ativo"));

    aba.classList.add("ativa");
    document.getElementById(aba.dataset.alvo).classList.add("ativo");
  });
});

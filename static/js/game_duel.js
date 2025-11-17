/**
 * Game Duel
 * JavaScript para interatividade do jogo
 */

// Este jogo é principalmente baseado em navegação via links
// Mas podemos adicionar funcionalidades extras aqui se necessário

document.addEventListener('DOMContentLoaded', function() {
    // Adiciona efeitos visuais aos cards de jogadores
    const jogadores = document.querySelectorAll('.jogador');
    
    jogadores.forEach(jogador => {
        jogador.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px) scale(1.02)';
        });
        
        jogador.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });
});


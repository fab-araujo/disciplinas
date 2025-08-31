import java.util.ArrayList;
import java.util.Random;

public class PrincipalDoGame {
    public static void main(String[] args) {
        //Criando a lista de objetos
        ArrayList<Objeto> objetos = new ArrayList<>();

        //Criando objetos que se movimentam
        Personagem Dayelle = new Personagem(1.0, 1.0, "Dayelle");
        Personagem Aghata = new Personagem(1.0, 1.0, "Aghata");
        Veiculo veiculoAzul = new Veiculo(4.0, 2.0, "Azul");
        Veiculo veiculoPreto = new Veiculo(4.0, 2.0, "Preto");
    

        //Populando a lista de objetos
        objetos.add(Dayelle);
        objetos.add(Aghata);
        objetos.add(new Personagem(1.5, 1.0, "Itania"));
        objetos.add(veiculoAzul);
        objetos.add(new Veiculo(4.0, 4.0, "Vermelho"));
        objetos.add(new Arvore(5.0, 5.0, 5.5));
        objetos.add(veiculoPreto);
        objetos.add(new Veiculo(4.0, 4.0, "Preto"));

        //Imprimindo cada elemento da lista de objetos
        for (Objeto objeto : objetos) {
            System.out.println(objeto);
        }

        System.out.println();

        //Criando lista de objetos que se movimentam
        ArrayList<Movimento> objetosComMovimento = new ArrayList<>();

        //Populando a lista de objetos que se movimentam
        objetosComMovimento.add(Dayelle);
        objetosComMovimento.add(Aghata);
        objetosComMovimento.add(veiculoAzul);
        objetosComMovimento.add(veiculoPreto);
        

        Random random = new Random(); //Objeto para sortear número
        for (Movimento objetoQueSeMove : objetosComMovimento) {
            //Movendo o objeto
            objetoQueSeMove.mover(random.nextDouble() * 100, random.nextDouble() * 100);
            //Imprimindo o objeto após o movimento
            System.out.println(objetoQueSeMove);
        }
    }
}




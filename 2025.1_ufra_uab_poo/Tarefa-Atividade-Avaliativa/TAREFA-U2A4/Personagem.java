public class Personagem extends Objeto implements Movimento {

    //TODO Encapsule o atributo abaixo
    String nome;

    public Personagem(double x, double y, String nome) {
        super(x, y);
        this.nome = nome;
    }

    public String getNome() {
        return nome;
    }

    public void setNome(String nome) {
        this.nome = nome;
    }

    //DICA: Considere utilizar como referência, o código da classe Veiculo
    //TODO: Sobrescreva o método da interface Movimento

    @Override
    public String toString() {
        final StringBuffer sb = new StringBuffer("Personagem{");
        sb.append("nome='").append(nome).append('\'');
        sb.append("x=").append(getX());
        sb.append(", y=").append(getY());
        sb.append('}');
        return sb.toString();
    }
}

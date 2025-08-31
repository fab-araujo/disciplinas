public class Arvore extends Objeto {

    private double altura;

    public Arvore(double x, double y, double altura) {
        //TODO Inclua a chamada ao construtor não padrão da superclasse
        this.altura = altura;
    }

    //TODO Crie os métodos de acesso (getter e setter) do atributo altura

    @Override
    public String toString() {
        final StringBuffer sb = new StringBuffer("Arvore{");
        sb.append("altura=").append(altura);
        sb.append(", x=").append(getX());
        sb.append(", y=").append(getY());
        sb.append('}');
        return sb.toString();
    }
}

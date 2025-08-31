//TODO Adicione a implementação da Interface Movimento
public class Veiculo extends Objeto {

    private String cor;

    public Veiculo(double x, double y, String cor) {
        super(x, y);
        this.cor = cor;
    }

    public String getCor() {
        return cor;
    }

    public void setCor(String cor) {
        this.cor = cor;
    }

    @Override
    public void mover(double x, double y) {
        setX(x);
        setY(y);
    }

    @Override
    public String toString() {
        final StringBuffer sb = new StringBuffer("Veiculo{");
        //DICA: Considere utilizar como referência, o código das classes Personagem ou Arvore
        //TODO Adicione no objeto sb todos os valores disponíveis em veículo
        sb.append('}');
        return sb.toString();
    }
}

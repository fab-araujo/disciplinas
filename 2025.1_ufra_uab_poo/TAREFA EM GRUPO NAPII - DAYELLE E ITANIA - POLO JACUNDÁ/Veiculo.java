public class Veiculo extends Objeto implements Movimento {

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
        sb.append("x=").append(getX());
        sb.append("y=").append(getY());
        sb.append("cor").append(cor).append('\'');
        sb.append('}');
        return sb.toString();
    }
}

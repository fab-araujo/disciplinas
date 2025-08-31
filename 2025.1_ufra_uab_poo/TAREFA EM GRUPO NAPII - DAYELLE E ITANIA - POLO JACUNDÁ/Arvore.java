public class Arvore extends Objeto {

    private double altura;

    public Arvore(double x, double y, double altura) {
        
        super(x, y);
        this.altura = altura;
    }

        public double getAltura() {
        return altura;
    }
    public void setAltura(double altura) {
        this.altura = altura;
    }

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

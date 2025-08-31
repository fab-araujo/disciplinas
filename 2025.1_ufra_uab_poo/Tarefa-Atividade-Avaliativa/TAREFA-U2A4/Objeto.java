public class Objeto {
    //TODO Encapsule os atributos abaixo
    double x;
    double y;

    public Objeto(double x, double y) {
        this.x = x;
        this.y = y;
    }

    public double getX() {
        return x;
    }

    public void setX(double x) {
        this.x = x;
    }

    //TODO Crie os métodos de acesso (getter e setter) do atributo y

    @Override
    public String toString() {
        final StringBuffer sb = new StringBuffer("Objeto{");
        sb.append("x=").append(x);
        sb.append(", y=").append(y);
        sb.append('}');
        return sb.toString();
    }
}

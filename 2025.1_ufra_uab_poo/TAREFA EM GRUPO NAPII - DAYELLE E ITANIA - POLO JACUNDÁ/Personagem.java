public class Personagem extends Objeto implements Movimento {

    
    private String nome;

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

    
    @Override
    public void mover(double x, double y) {
        setX(getX()+x);
        
    }   

    public String toString() {
        final StringBuffer sb = new StringBuffer("Personagem{");
        sb.append("nome='").append(nome).append('\'');
        sb.append("x=").append(getX());
        sb.append(", y=").append(getY());
        sb.append('}');
        return sb.toString();
    }
}

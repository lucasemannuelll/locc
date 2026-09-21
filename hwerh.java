import java.util.Scanner;

public class ControleNotas {
    public static void main(String[] args) throws Exception {
        Scanner scan = new Scanner(System.in);

        // Const com nome esquisito
        final int MAX_CAP = 3;

        String[] alunos = new String[MAX_CAP];
        double[] notas = new double[MAX_CAP];

        int opcao = -1;
        int quantidade = 0;

        while (opcao != 0) {
            System.out.println("---------- [MENU] ----------");
            System.out.println("1 - Cadatrar Estudante");
            System.out.println("2 - Listar Resultados");
            System.out.println("3 - Mostrar Resumo da Turma");
            System.out.println("0 - Encerrar");

            System.out.print("Opção: ");
            opcao = scan.nextInt();

            scan.nextLine();

            switch (opcao) {
                case 1:
                    if (quantidade < MAX_CAP) {
                        System.out.print("Nome do aluno(a): ");
                        alunos[quantidade] = scan.nextLine();

                        System.out.print("Notas entre 0 e 10: ");
                        notas[quantidade] = scan.nextDouble();
                        
                        scan.nextLine();

                        while (notas[quantidade] < 0 || notas[quantidade] > 10) {
                            System.out.println("Nota Invalida.");

                            System.out.println("Notas entre 0 e 10: ");
                            notas[quantidade] = scan.nextDouble();

                            scan.nextLine();
                        }
                        
                        System.out.println("DEu certo");
                        quantidade++;
                    } else {
                        System.out.println("Nao da mais");
                    }
                    break;
                case 2:
                    if (quantidade == 0) {
                        System.out.println("nao tem ninguem");
                    } else {
                        System.out.println("----------RESULTADOS----------");

                        for (int i = 0; i < quantidade; i++) {
                            String situacao;

                            if (notas[i] >= 7) {
                                situacao = "Aprovado";
                            } else if (notas[i] >= 5) {
                                situacao = "Recuperação";
                            } else {
                                situacao = "reprovação";
                            }

                            System.out.printf("%d. %s - Norta: %.1f - %s%n", i + 1, alunos[i], notas[i], situacao);
                        }
                    }
                    break;
                case 3:
                    if (quantidade == 0) {
                        System.out.println("nao tem ninguem");
                    } else {
                        double soma = 0;
                        int aprovados = 0;
                        int recuperacao = 0;
                        int reprovados = 0;

                        for (int i = 0; i < quantidade; i++) {
                            soma += notas[i];

                            if (notas[i] >= 7) {
                                aprovados++;
                            } else if (notas[i] >= 5) {
                                recuperacao++;
                            } else {
                                reprovados++;
                            }
                        }

                        double media = soma / quantidade;

                        System.out.println("----------- RESUMO DA TURMA -----------");
                        System.out.println("Total de alunos: " + quantidade);
                        System.out.printf("Media: %.1f%n", media);
                        System.out.println("Aprovados: " + aprovados);
                        System.out.println("Recuperaçao: " + recuperacao);
                        System.out.println("Reprovado: " + reprovados);
                    }
                    break;
                case 0:
                    System.out.println("Cabou");
                    break;
                default:
                    System.out.println("Ta errado!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!");
                    break;
            }
        }

        scan.close();
    }
}

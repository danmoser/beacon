/* ccdrap_e.f -- translated by f2c (version 20050501).
   You must link the resulting object file with libf2c:
	on Microsoft Windows system, link with libf2c.lib;
	on Linux or Unix systems, link with .../path/to/libf2c.a -lm
	or, if you install libf2c.a in a standard place, with -lf2c -lm
	-- in that order, at the end of the command line, as in
		cc *.o -lf2c -lm
	Source for libf2c is in /netlib/f2c/libf2c.zip, e.g.,

		http://www.netlib.org/f2c/libf2c.zip
*/

#include "f2c.h"

/* Table of constant values */

static integer c__1 = 1;
static integer c__2 = 2;
static integer c__3 = 3;
static integer c__4 = 4;
static integer c__5 = 5;
static integer c__9 = 9;


/* 	program phot_pol (ver 1.0 - agosto/1999) */

/* 	fortran-iraf para fazer fotometria de campos com calcita */

/* 	Usa pccd do Antonio Mario Magalhaes */


/* 	uso: phot_pol arq_mag */


/* Resumo: */

/* 	1. le arquivo com contagens - saida do phot */


/* Main program */ int MAIN__()
{
    /* Format strings */
    static char fmt_11[] = "(a,300g14.8)";

    /* System generated locals */
    integer i__1, i__2, i__3, i__4;
    icilist ici__1;
    olist o__1;
    cllist cl__1;

    /* Builtin functions */
    integer s_wsle(), do_lio(), e_wsle();
    /* Subroutine */ int s_stop();
    integer f_open(), s_rsfe(), do_fio(), e_rsfe(), i_indx();
    /* Subroutine */ int s_copy();
    integer s_rsli(), e_rsli(), f_clos(), s_wsfe(), e_wsfe();

    /* Local variables */
    static doublereal a[60];
    static integer i__, j, k, l;
    static doublereal ap[18], ane[1800000]	/* was [100][1000][18] */, 
	    ano[1800000]	/* was [100][1000][18] */;
    static integer nap, ier, nhw;
    static doublereal anes[1800]	/* was [100][1][18] */;
    static char line[380];
    static doublereal anos[1800]	/* was [100][1][18] */, skye[100000]	
	    /* was [100][1000] */, skyo[100000]	/* was [100][1000] */, areae[
	    1800000]	/* was [100][1000][18] */;
    static char image[12];
    static doublereal areao[1800000]	/* was [100][1000][18] */;
    static integer nargs;
    static doublereal skyes[100]	/* was [100][1] */, skyos[100]	/* 
	    was [100][1] */;
    extern /* Subroutine */ int clargc_();
    static doublereal arease[100000]	/* was [100][1000] */, areaes[1800]	
	    /* was [100][1][18] */;
    extern /* Subroutine */ int clargi_(), clnarg_();
    static char arq_in__[60];
    static doublereal areaso[100000]	/* was [100][1000] */, areaos[1800]	
	    /* was [100][1][18] */;
    extern /* Subroutine */ int imemsg_();
    static doublereal errmsg;
    static integer nstars;
    static doublereal areases[100]	/* was [100][1] */, areasos[100]	
	    /* was [100][1] */;
    static char arq_out__[60];

    /* Fortran I/O blocks */
    static cilist io___8 = { 0, 6, 0, 0, 0 };
    static cilist io___9 = { 0, 6, 0, 0, 0 };
    static cilist io___10 = { 0, 6, 0, 0, 0 };
    static cilist io___11 = { 0, 6, 0, 0, 0 };
    static cilist io___12 = { 0, 6, 0, 0, 0 };
    static cilist io___13 = { 0, 6, 0, 0, 0 };
    static cilist io___16 = { 0, 8, 0, "(a)", 0 };
    static cilist io___27 = { 0, 8, 0, "(a)", 0 };
    static cilist io___40 = { 0, 8, 0, fmt_11, 0 };
    static cilist io___41 = { 0, 8, 0, fmt_11, 0 };
    static cilist io___43 = { 0, 6, 0, "('Erro: ',a80)", 0 };




/*       Numero maximo de aberturas= 18 */
/*       Numero de estrelas=100    *    06 Jun 95    *    VEM - CVR */

/*       ano(# estrelas, pos. lamina, aberturas) */



/* 	lendo parametros da linha de comando */

    clnarg_(&nargs);
    if (nargs == 5) {
	clargc_(&c__1, arq_in__, &ier, (ftnlen)60);
	if (ier != 0) {
	    goto L100;
	}
	clargc_(&c__2, arq_out__, &ier, (ftnlen)60);
	if (ier != 0) {
	    goto L100;
	}
	clargi_(&c__3, &nstars, &ier);
	if (ier != 0) {
	    goto L100;
	}
	clargi_(&c__4, &nhw, &ier);
	if (ier != 0) {
	    goto L100;
	}
	clargi_(&c__5, &nap, &ier);
	if (ier != 0) {
	    goto L100;
	}
    } else {
	s_wsle(&io___8);
	do_lio(&c__9, &c__1, "No. de parametros incorreto em PHOT_POL", (
		ftnlen)39);
	e_wsle();
	s_wsle(&io___9);
	do_lio(&c__9, &c__1, " ", (ftnlen)1);
	e_wsle();
	s_wsle(&io___10);
	do_lio(&c__9, &c__1, "Uso: phot_pol ??? ", (ftnlen)18);
	e_wsle();
	goto L110;
    }

/* 	Verificando se valores de variaveis estao dentro do intervalo */
/* 		permitido */

    if (nap > 18) {
	s_wsle(&io___11);
	do_lio(&c__9, &c__1, "Numero de aberturas fora do limite", (ftnlen)34)
		;
	e_wsle();
	s_stop("", (ftnlen)0);
    }
    if (nstars > 100) {
	s_wsle(&io___12);
	do_lio(&c__9, &c__1, "Numero de estrelas fora do limite", (ftnlen)33);
	e_wsle();
	s_stop("", (ftnlen)0);
    }
    if (nhw > 1000) {
	s_wsle(&io___13);
	do_lio(&c__9, &c__1, "Numero de laminas fora do limite", (ftnlen)32);
	e_wsle();
	s_stop("", (ftnlen)0);
    }

/* lendo arquivos com fotometria */

    o__1.oerr = 0;
    o__1.ounit = 8;
    o__1.ofnmlen = 60;
    o__1.ofnm = arq_in__;
    o__1.orl = 0;
    o__1.osta = "old";
    o__1.oacc = 0;
    o__1.ofm = 0;
    o__1.oblnk = 0;
    f_open(&o__1);

    i__1 = nhw;
    for (i__ = 1; i__ <= i__1; ++i__) {
	i__2 = nstars;
	for (j = 1; j <= i__2; ++j) {
/* 			print*, j */
	    s_rsfe(&io___16);
	    do_fio(&c__1, line, (ftnlen)380);
	    e_rsfe();
	    s_copy(image, line, (ftnlen)12, (ftnlen)(i_indx(line, " ", (
		    ftnlen)380, (ftnlen)1)));
/* 			print*, line */
	    i__3 = i_indx(line, " ", (ftnlen)380, (ftnlen)1) - 1;
	    ici__1.icierr = 0;
	    ici__1.iciend = 0;
	    ici__1.icirnum = 1;
	    ici__1.icirlen = 380 - i__3;
	    ici__1.iciunit = line + i__3;
	    ici__1.icifmt = 0;
	    s_rsli(&ici__1);
	    i__4 = nap * 3 + 2;
	    for (l = 1; l <= i__4; ++l) {
		do_lio(&c__5, &c__1, (char *)&a[l - 1], (ftnlen)sizeof(
			doublereal));
	    }
	    e_rsli();
/*      			print*,a */
/* 			stop */
	    skyo[j + i__ * 100 - 101] = a[0];
	    areaso[j + i__ * 100 - 101] = a[1];
/* 			print* */
/* 			print*, skyo(j,i) */
/* 			print* */
	    if (i__ == 1 && j == 1) {
		i__3 = nap;
		for (k = 1; k <= i__3; ++k) {
		    ap[k - 1] = a[k + 1];
		}
	    }
	    i__3 = nap;
	    for (k = 1; k <= i__3; ++k) {
		ano[j + (i__ + k * 1000) * 100 - 100101] = a[nap + 2 + k - 1];
	    }
	    i__3 = nap;
	    for (k = 1; k <= i__3; ++k) {
		areao[j + (i__ + k * 1000) * 100 - 100101] = a[nap + 2 + nap 
			+ k - 1];
	    }

	    s_rsfe(&io___27);
	    do_fio(&c__1, line, (ftnlen)380);
	    e_rsfe();
	    s_copy(image, line, (ftnlen)12, (ftnlen)(i_indx(line, " ", (
		    ftnlen)380, (ftnlen)1)));
	    i__3 = i_indx(line, " ", (ftnlen)380, (ftnlen)1) - 1;
	    ici__1.icierr = 0;
	    ici__1.iciend = 0;
	    ici__1.icirnum = 1;
	    ici__1.icirlen = 380 - i__3;
	    ici__1.iciunit = line + i__3;
	    ici__1.icifmt = 0;
	    s_rsli(&ici__1);
	    i__4 = nap * 3 + 2;
	    for (l = 1; l <= i__4; ++l) {
		do_lio(&c__5, &c__1, (char *)&a[l - 1], (ftnlen)sizeof(
			doublereal));
	    }
	    e_rsli();
	    skye[j + i__ * 100 - 101] = a[0];
	    arease[j + i__ * 100 - 101] = a[1];
	    i__3 = nap;
	    for (k = 1; k <= i__3; ++k) {
		ane[j + (i__ + k * 1000) * 100 - 100101] = a[nap + 2 + k - 1];
	    }
	    i__3 = nap;
	    for (k = 1; k <= i__3; ++k) {
		areae[j + (i__ + k * 1000) * 100 - 100101] = a[nap + 2 + nap 
			+ k - 1];
	    }
	}
    }

    cl__1.cerr = 0;
    cl__1.cunit = 8;
    cl__1.csta = 0;
    f_clos(&cl__1);


/* 	Calculando soma para cada todas as exposicoes */


    o__1.oerr = 0;
    o__1.ounit = 8;
    o__1.ofnmlen = 60;
    o__1.ofnm = arq_out__;
    o__1.orl = 0;
    o__1.osta = "new";
    o__1.oacc = 0;
    o__1.ofm = 0;
    o__1.oblnk = 0;
    f_open(&o__1);
    i__1 = nstars;
    for (j = 1; j <= i__1; ++j) {
	i__2 = nap;
	for (k = 1; k <= i__2; ++k) {
	    anos[j + (k + 1) * 100 - 201] = (float)0.;
	    anes[j + (k + 1) * 100 - 201] = (float)0.;
	    areaos[j + (k + 1) * 100 - 201] = (float)0.;
	    areaes[j + (k + 1) * 100 - 201] = (float)0.;
	    i__3 = nhw;
	    for (i__ = 1; i__ <= i__3; ++i__) {
		anos[j + (k + 1) * 100 - 201] += ano[j + (i__ + k * 1000) * 
			100 - 100101];
		anes[j + (k + 1) * 100 - 201] += ane[j + (i__ + k * 1000) * 
			100 - 100101];
		areaos[j + (k + 1) * 100 - 201] += areao[j + (i__ + k * 1000) 
			* 100 - 100101];
		areaes[j + (k + 1) * 100 - 201] += areae[j + (i__ + k * 1000) 
			* 100 - 100101];
	    }
	    areaos[j + (k + 1) * 100 - 201] /= nhw;
	    areaes[j + (k + 1) * 100 - 201] /= nhw;
	}
    }
    i__1 = nstars;
    for (j = 1; j <= i__1; ++j) {
	skyos[j - 1] = (float)0.;
	skyes[j - 1] = (float)0.;
	areasos[j - 1] = (float)0.;
	areases[j - 1] = (float)0.;
	i__2 = nhw;
	for (i__ = 1; i__ <= i__2; ++i__) {
	    skyos[j - 1] += skyo[j + i__ * 100 - 101];
	    skyes[j - 1] += skye[j + i__ * 100 - 101];
	    areasos[j - 1] += areaso[j + i__ * 100 - 101];
	    areases[j - 1] += arease[j + i__ * 100 - 101];
	}
	areasos[j - 1] /= nhw;
	areases[j - 1] /= nhw;
    }
/* Escreve Resultado */
/* L10: */
/* L11: */

    i__1 = nstars;
    for (j = 1; j <= i__1; ++j) {
	s_wsfe(&io___40);
	do_fio(&c__1, "CCDRAP.o ", (ftnlen)9);
	do_fio(&c__1, (char *)&skyos[j - 1], (ftnlen)sizeof(doublereal));
	do_fio(&c__1, (char *)&areasos[j - 1], (ftnlen)sizeof(doublereal));
	i__2 = nap;
	for (k = 1; k <= i__2; ++k) {
	    do_fio(&c__1, (char *)&ap[k - 1], (ftnlen)sizeof(doublereal));
	}
	i__3 = nap;
	for (k = 1; k <= i__3; ++k) {
	    do_fio(&c__1, (char *)&anos[j + (k + 1) * 100 - 201], (ftnlen)
		    sizeof(doublereal));
	}
	i__4 = nap;
	for (k = 1; k <= i__4; ++k) {
	    do_fio(&c__1, (char *)&areaos[j + (k + 1) * 100 - 201], (ftnlen)
		    sizeof(doublereal));
	}
	e_wsfe();
	s_wsfe(&io___41);
	do_fio(&c__1, "CCDRAP.e ", (ftnlen)9);
	do_fio(&c__1, (char *)&skyes[j - 1], (ftnlen)sizeof(doublereal));
	do_fio(&c__1, (char *)&areases[j - 1], (ftnlen)sizeof(doublereal));
	i__2 = nap;
	for (k = 1; k <= i__2; ++k) {
	    do_fio(&c__1, (char *)&ap[k - 1], (ftnlen)sizeof(doublereal));
	}
	i__3 = nap;
	for (k = 1; k <= i__3; ++k) {
	    do_fio(&c__1, (char *)&anes[j + (k + 1) * 100 - 201], (ftnlen)
		    sizeof(doublereal));
	}
	i__4 = nap;
	for (k = 1; k <= i__4; ++k) {
	    do_fio(&c__1, (char *)&areaes[j + (k + 1) * 100 - 201], (ftnlen)
		    sizeof(doublereal));
	}
	e_wsfe();
    }
    cl__1.cerr = 0;
    cl__1.cunit = 8;
    cl__1.csta = 0;
    f_clos(&cl__1);

    goto L120;
L100:
    imemsg_(&ier, &errmsg);
    s_wsfe(&io___43);
    do_fio(&c__1, (char *)&errmsg, (ftnlen)sizeof(doublereal));
    e_wsfe();
L110:
    s_stop("", (ftnlen)0);
L120:
    ;
} /* MAIN__ */

/* Main program alias */ int phot_pol_e__ () { MAIN__ (); }

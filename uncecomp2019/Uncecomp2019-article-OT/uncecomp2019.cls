%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% ECCOMAS Class for LaTeX files                 v1.1 Feb-23-2000 %%
%%                                                                %%
%% The regular article class commands still exist and may be used.%%
%% 10pt, 11pt and twocolumn options are disabled.                 %%
%%                                                                %%
%% \maketitle make the first page automatically                   %%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{uncecomp2019}[2006/06/05-08 ECCOMAS paper class]

\DeclareOption{10pt}{\OptionNotUsed}
\DeclareOption{11pt}{\OptionNotUsed}
\DeclareOption{twocolumn}{\OptionNotUsed}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{article}}

\DeclareOption{dvips}{%
  \PassOptionsToPackage{dvips}{hyperref}}
\DeclareOption{pdftex}{%
  \PassOptionsToPackage{pdftex}{hyperref}}
\DeclareOption{dvipdfm}{%
  \PassOptionsToPackage{dvipdfm}{hyperref}}
\DeclareOption{dvips}{%
  \PassOptionsToPackage{dvips}{graphicx}}
\DeclareOption{pdftex}{%
  \PassOptionsToPackage{pdftex}{graphicx}}
\DeclareOption{dvipdfm}{%
  \PassOptionsToPackage{dvipdfm}{graphicx}}

\ProcessOptions\relax

\LoadClass[a4paper,12pt]{article}

\RequirePackage{hyperref}
\RequirePackage{calc}
\RequirePackage{indentfirst}
\RequirePackage{url}
\RequirePackage{graphicx}
\RequirePackage{times}

%% Title
\renewcommand{\maketitle}{%
 \newpage
 \thispagestyle{plain}
 \begin{minipage}[t][26mm][t]{155mm}
  \begin{flushright}
   \scriptsize
   UNCECOMP 2019\\
   3$^{\textrm{rd}}$ ECCOMAS Thematic Conference on \\
   Uncertainty Quantification in Computational Sciences and Engineering \\
   M. Papadrakakis, V. Papadopoulos, G. Stefanou (eds.) \\
   Crete, Greece, 24–-26 June 2019
  \end{flushright}
 \end{minipage}
 \begin{center}%
  {%3
   \fontsize{14}{16}\selectfont
   \bfseries
   \MakeUppercase{\@title}
   \par
  }%3
  \vspace{18pt}%
  {%4
\fontsize{12}{14}\selectfont
   \bfseries\@author
   \par
  }%4
  \vspace{14pt}%
  {%5
\fontsize{11}{12}\selectfont
   \def\and{\\\vspace{14pt}}
   \normalfont\@address
   \par
  }%5
 \end{center}
 \vspace{18pt}%
 \noindent\textbf{Keywords:\space}\@keywords
 \par
 \vspace{18pt}%
 \noindent\textbf{Abstract.\space}{\textit\@abstract}
 \par
 \vfill
 \newpage
}% End of \@maketitle

\def\author{\@ifnextchar[{\@getshortauthor}{\@getauthor}}
\def\@getauthor#1{\gdef\@author{#1}\gdef\@shortauthor{#1}}
\def\@getshortauthor[#1]#2{\gdef\@shortauthor{#1}\gdef\@author{#2}}

\newcommand{\address}[1]{\gdef\@address{#1}}

\newcommand{\keywords}[1]{\gdef\@keywords{#1}}

\renewcommand{\abstract}[1]{\gdef\@abstract{#1}}

\newcommand{\heading}[1]{\gdef\@heading{#1}}

\def\ps@myheadings{%
    \def\@oddfoot{\normalfont\hfil\thepage\hfil}
    \let\@evenfoot\@oddfoot
    \def\@evenhead{%
        \parbox[t][11.5pt][t]{\textwidth}{%
        \centering
        \normalfont
        \fontsize{10}{10}\selectfont
        \@heading\\
\vspace{-.2cm}
        \rule{\textwidth}{1pt}%
     }
    }%
    \let\@oddhead\@evenhead
    \let\@mkboth\@gobbletwo
    \let\sectionmark\@gobble
    \let\subsectionmark\@gobble
}

\def\sectionLevel{1}
\def\sectionIndent{0pt}
\def\sectionSpaceBefore{12pt}
\def\sectionSpaceAfter{6pt}
\def\sectionStyle{\normalsize\bfseries\MakeUppercase}

\renewcommand{\section}{%
  \@startsection{section}{\sectionLevel}{\sectionIndent}{\sectionSpaceBefore}%
                {\sectionSpaceAfter}{\sectionStyle}}%

\def\sectionLevel{2}
\def\sectionIndent{0pt}
\def\sectionSpaceBefore{12pt}
\def\sectionSpaceAfter{6pt}
\def\sectionStyle{\normalsize\bfseries}

\renewcommand{\subsection}{%
  \@startsection{subsection}{\sectionLevel}{\sectionIndent}{\sectionSpaceBefore}%
                {\sectionSpaceAfter}{\sectionStyle}}%

\renewcommand{\@makecaption}[2]{%
  \vskip\abovecaptionskip
  \sbox\@tempboxa{\normalsize\fontsize{10}{12}\selectfont #1: #2}%
  \ifdim \wd\@tempboxa >\hsize
    \normalsize\fontsize{10}{12}\selectfont #1: #2\par
  \else
    \global \@minipagefalse
    \hb@xt@\hsize{\hfil\box\@tempboxa\hfil}%
  \fi
  \vskip\belowcaptionskip}

\renewenvironment{thebibliography}[1]
  {\bigskip
  \section*{\MakeUppercase\refname\@mkboth{\MakeUppercase\refname}{\MakeUppercase\refname}}%
  \list{\@biblabel{\@arabic\c@enumiv}}%
        {\settowidth\labelwidth{\@biblabel{#1}}%
         \leftmargin\labelwidth
         \advance\leftmargin\labelsep
         \@openbib@code
         \usecounter{enumiv}%
         \let\p@enumiv\@empty
         \renewcommand\theenumiv{\@arabic\c@enumiv}}%
   \sloppy
   \clubpenalty4000
   \@clubpenalty \clubpenalty
   \widowpenalty4000%
   \sfcode`\.\@m}
  {\def\@noitemerr
   {\@latex@warning{Empty `thebibliography' environment}}%
   \endlist}
\setlength{\oddsidemargin}{0mm}
\setlength{\topmargin}{-10mm}
\setlength{\textheight}{240mm}
\setlength{\textwidth}{160mm}
\setlength{\textfloatsep}{12pt}
\setlength{\abovedisplayskip}{6pt}
\setlength{\belowdisplayskip}{6pt}
\setlength{\parindent}{5mm}
\setlength{\abovecaptionskip}{6pt}
\setlength{\belowcaptionskip}{6pt}
\setlength{\itemsep}{0pt}

\AtBeginDocument{%
  \pagestyle{myheadings}
  \maketitle
  \let\maketitle\relax
}

\endinput

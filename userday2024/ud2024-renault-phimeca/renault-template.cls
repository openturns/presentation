% RENAULT BEAMER TEMPLATE
%
% Cette classe de document est basee sur [beamer].
%
% This program is free software: you can redistribute it and/or modify
% it under the terms of the GNU General Public License as published by
% the Free Software Foundation
%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%renault
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{renault-template}[04/05/2020 v1.0]

\LoadClass[dvipsnames, usenames, 9pt, aspectratio=169]{beamer}

\RequirePackage[english]{babel}
\RequirePackage[utf8]{inputenc}
\RequirePackage[T1]{fontenc}
\RequirePackage{xspace}
\RequirePackage{etoolbox}
\RequirePackage{graphicx} 
\RequirePackage{xcolor}
\RequirePackage{enumitem}
\RequirePackage[autolanguage]{numprint}
\RequirePackage{pifont}
\RequirePackage[format=hang, justification=RaggedRight]{caption}
\RequirePackage{subfigure}
\RequirePackage{multirow}
\RequirePackage{eso-pic}
\RequirePackage{epsfig}
\RequirePackage{bm}
\RequirePackage{hyperref}
\RequirePackage{pgf, tikz}
\usetikzlibrary{calc, shapes, arrows, fit, shadows, overlay-beamer-styles}


\tikzset{
  highlight on/.style={alt={#1{fill=RED!80!BLACK,color=RED!80!BLACK}{fill=GREY01!30!WHITE,color=GREY01!30!WHITE}}},
}

% Load theme 
\usetheme[compress]{Dresden}

% Set size
\setbeamersize{text margin left=0.5cm, text margin right=0.5cm}


%% Define Colors
%-----------------------------------------------------------------------
% Corporate Colours
\definecolor{YELLOW}{RGB}{255, 204, 051}
\definecolor{WHITE}{RGB}{255, 255, 255}
\definecolor{BLACK}{RGB}{000, 000, 000}
\definecolor{GREY01}{RGB}{061, 057, 053}
\definecolor{GREY02}{RGB}{135, 135, 133}
\definecolor{GREY03}{RGB}{151, 153, 155}
\definecolor{GREY04}{RGB}{207, 201, 196}

% Secondary Colors
\definecolor{RED}{RGB}{200, 014, 014}
\definecolor{GREEN}{RGB}{155, 200, 020}
\definecolor{BLUE}{RGB}{090, 120, 190}
\definecolor{INDIGO}{RGB}{055, 190, 215}
\definecolor{ORANGE}{RGB}{255, 125, 020}
\definecolor{ANIS}{RGB}{220, 220, 000}

% Brands Colours
%\definecolor{RENAULT}{RGB}{255, 204, 051}

\definecolor{RENAULT}{RGB}{151, 153, 155}

\definecolor{DACIA}{RGB}{000, 050, 146}
\definecolor{RSM}{RGB}{090, 040, 160}
\definecolor{ALPINE}{RGB}{000, 091, 187}
\definecolor{LADA}{RGB}{255, 125, 020}

% Set Colors of Beamer structure and foot
\setbeamercolor{structure}{bg=RENAULT, fg=white}
\setbeamercolor{foot}{bg=WHITE, fg=BLACK}
%-----------------------------------------------------------------------

%-----------------------------------------------------------------------
%% Define new commands
\newcommand{\source}[1]{\caption*{\textcolor{RENAULT}{Source:} {#1}} }

\newcommand{\overbar}[1]{\mkern 1.5mu\overline{\mkern-1.5mu#1\mkern-1.5mu}\mkern 1.5mu}

\newcommand{\sommaire}[1]{\gdef\@sommaire{#1}}
\sommaire{}

\newcommand{\confidentiality}[1]{\gdef\@confidentiality{#1}}
\confidentiality{}

%-----------------------------------------------------------------------
%% Set Beamer templates %%

% Change the items in the Contents
%\setbeamertemplate{section in toc}[sections numbered]
\setbeamertemplate{section in toc}{%
  \hspace{0.5em}{\color{RENAULT}\rule[0ex]{7pt}{7pt}}~
  \color{black}
  %\rlap{\hskip-3em\inserttocsectionnumber.\inserttocsubsectionnumber.\inserttocsubsubsectionnumber}%
 %\inserttocsubsubsection
  \inserttocsection
  \par}

% Change the footline
\setbeamertemplate{footline}{
\leavevmode%
%\hbox{
%\vline height 9pt depth 2pt width 0.5pt
%\begin{beamercolorbox}[wd=.4\paperwidth,ht=3ex,dp=2ex,center]{foot}%
%  \insertshortinstitute ~\textemdash~ \insertshortauthor  
%\end{beamercolorbox}% 
%\vline height 9pt depth 2pt width 0.5pt
%\begin{beamercolorbox}[wd=.15\paperwidth,ht=3ex,dp=2ex,center]{foot}%
%  \insertshortdate{}
%\end{beamercolorbox}%
%\vline height 9pt depth 2pt width 0.5pt
%\begin{beamercolorbox}[wd=.2\paperwidth,ht=3ex,dp=2ex,center]{foot}%
%  \fcolorbox{BLACK}{WHITE}{\@confidentiality}
%\end{beamercolorbox}%
%\vline height 9pt depth 2pt width 0.5pt
%\begin{beamercolorbox}[wd=.08\paperwidth,ht=3ex,dp=2ex,center]{foot}%
%  \insertframenumber{} / \inserttotalframenumber
%\end{beamercolorbox}}%
\hspace{13.5cm}
%\begin{beamercolorbox}[wd=.12\paperwidth,ht=3ex,dp=2ex,right]{foot}%
  \includegraphics[scale=0.03]{figure/grpe_rno_black}
%\end{beamercolorbox}%

%\vskip0pt%
}

\setbeamertemplate{navigation symbols}{}
\setbeamertemplate{section/subsection in toc}[square]

% Define headline (colors + space between items)
\defbeamertemplate*{headline}{miniframes theme no subsection}
{%
  \begin{beamercolorbox}[colsep=1.5pt]{upper separation line head}
  \end{beamercolorbox}
  \begin{beamercolorbox}{structure}
    \vskip3pt\insertnavigation{2.3cm}\vskip4pt
  \end{beamercolorbox}%
  \begin{beamercolorbox}[colsep=1.5pt]{lower separation line head}
  \end{beamercolorbox}
}
%-----------------------------------------------------------------------




%-----------------------------------------------------------------------
% Configure what happen every time a new section begins
%\AtBeginSection[]
%{
%  \begin{frame}{\@sommaire}
    %\tableofcontents[currentsection, hideallsubsections]
%    \tableofcontents[currentsection]
%  \end{frame} 
%}




%%%%%%%%%%%%%%%%%%%

\newcommand{\mysquare}{{\color{RENAULT}\rule[0ex]{5pt}{5pt}}~}

\setbeamercolor{block body}{bg=RENAULT!10!white}
\newcommand{\labelitemi}{
  \mysquare
}

\newcommand{\labelitemii}{
{\color{BLACK}\rule[0ex]{5pt}{5pt}}~
}


%-----------------------------------------------------------------------

%% TITLE
\setbeamerfont{title}{series=\bfseries,size={\fontsize{26}{24}}}
\setbeamerfont{section title}{series=\bfseries,size={\fontsize{12}{12}}}

\defbeamertemplate*{title page}{customized}[1][]
{ 
  \includegraphics[scale=0.3]{figure/grpe_rno_white.png}
  \par
  \vspace{4cm}
  \usebeamercolor[white]{}\usebeamerfont{title}\inserttitle\par
  \usebeamerfont{subtitle}
  \usebeamercolor[fg]{subtitle}\insertsubtitle\par
  \bigskip
  \usebeamerfont{author}\insertauthor\par
  \usebeamerfont{institute}\insertinstitute\par
  \usebeamerfont{date}\insertdate\par
  \usebeamercolor[fg]{titlegraphic}\inserttitlegraphic
}

%-----------------------------------------------------------------------

%% SECTION
\setbeamertemplate{section page}{
    \begin{tabular}{cc}
        \begin{minipage}{0.45 \paperwidth}
            \flushleft
            \fontsize{20}{7.2}\selectfont
            %\insertsectionnumber
            %\vspace{0.5cm}
            %\newline
            \usebeamerfont{section title}
            \insertsection
            \\[0.4cm]
            %\tableofcontents[sectionstyle=hide/hide%
%,currentsubsection,subsectionstyle=hide/show]
            %\usebeamerfont{part title}
            
            
            %\end{beamercolorbox}
        \end{minipage}
        &  
        \begin{minipage}{0.5 \paperwidth}
            \flushright
            \begin{tikzpicture}
                \node[opacity=1, inner sep=-2pt]{
                \includegraphics[height=\paperheight]{figure/image2.jpg}};
            \end{tikzpicture}
        \end{minipage}        
    \end{tabular}
}

\AtBeginSection{\frame{\sectionpage}}
%\AtBeginSubsection{\frame{\subsectionpage}}

function Final=R0_eigen_for_InterventionNode()
%A=dlmread('/Users/halehashki/Haleh/Thesis/Paper/codes/data/barabasi_albert_Network/Networks2/Networks/Network90.txt');
A=dlmread('/Users/halehashki/Haleh/Thesis/Paper/codes/data/erdos_renyi_Network/Networks2/Networks/Network9.txt');
%A=dlmread('/Users/halehashki/Haleh/Thesis/Paper/codes/data/watts_strogatz_Network/Networks2/Networks/Network9.txt');




Final=zeros(5,7);


T=cal_R0_star(A);
Final(1,:)=T;

L=diag(sum(A))-A;
[V E]=eig(L);
[ES EI]=sort(diag(E),'descend');
EH=V(:,EI(1));
[va nodes]=sort(EH,'descend');  %% values and index of the sortes eigenvector of the largest eigenvale



A=intervention(A,nodes(1:100));
T=cal_R0_star(A);
Final(2,:)=T;


A=intervention(A,nodes(1:200));
T=cal_R0_star(A);
Final(3,:)=T;

A=intervention(A,nodes(1:300));
T=cal_R0_star(A);
Final(4,:)=T;

A=intervention(A,nodes(1:400));
T=cal_R0_star(A);
Final(5,:)=T;



end

function A=intervention(A, nodes)


  for i=1:size(nodes,1)
      A(i,:)=0;
      A(:,i)=0;
  end


end


function T= cal_R0_star(A)

beta=.005;
gamma=.05;
n=1000;

S=sum(A);
u=unique(S);
count=histc(S,unique(S));
p=count/n;
k=u*p';
u2=u-1;
u3=u2.*u;
k2=u3*p';


R0=(beta/(beta+gamma)) .* ((k2-k)/k);
%T=[k,k2,R0];


%[s v d]=svd(A);
%s=diag(v);
s=eig(A);


for j=1:size(s,1)-1
    e(j)=abs(s(j+1)-s(j));
end

m=1;
while (e(m))  > .005   %.005
    m=m+1;
end


m=m-1;
d=(s(m)-s(1))/(m-1);

R0_star=R0 * (1/abs(d));
R0_star1=R0 * (1/sqrt(abs(d)));


T=[k k2 m d R0 R0_star R0_star1];
end
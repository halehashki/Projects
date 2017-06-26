function cal_R0_star_eigenvalue()

%A=dlmread('/Users/halehashki/Haleh/Thesis/Paper/codes/data/barabasi_albert_Network/Networks2/Networks/Network90.txt');
%A=dlmread('/Users/halehashki/Haleh/Thesis/Paper/codes/data/erdos_renyi_Network/Networks2/Networks/Network9.txt');
A=dlmread('/Users/halehashki/Haleh/Thesis/Paper/codes/data/watts_strogatz_Network/Networks2/Networks/Network9.txt');

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


[s v d]=svd(A);
s=diag(v);


for j=1:size(s,1)-1
    e(j)=abs(s(j+1)-s(j));
end

m=1;
while (e(m))  > .005   %.005
    m=m+1;
end


m=m-1;
d=(s(m)-s(1))/(m-1);

R0_star1=R0 * (1/abs(d));


T1=[m d R0_star1]

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

R0_star2=R0 * (1/abs(d));
R0_star3=R0 * (1/sqrt(abs(d)));

T2=[m d R0_star2 R0_star3]

end
